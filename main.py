import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time

# Setup custom logger
logger = logging.getLogger('web_scraper')
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('test2.log')
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)


def select_season(driver, year):
    """
    Function to select the appropriate season year from the dropdown.
    """
    try:
        # Open the season dropdown menu
        logger.info("Attempting to open the season dropdown menu.")

        # Use JavaScript to ensure visibility and click
        season_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.customSelecBox div.cSBDisplay"))
        )
        driver.execute_script("arguments[0].click();", season_dropdown)  # Use JavaScript click as a fallback

        # Wait for the dropdown options to become visible
        logger.info(f"Looking for the season year: {year}")
        season_year_option = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.cSBListItems[data-val='{year}']"))
        )

        # Click on the correct season year
        logger.info(f"Clicking the season year: {year}")
        driver.execute_script("arguments[0].click();", season_year_option)  # Use JavaScript click as a fallback

        logger.info(f"Successfully selected season year {year}.")
    except Exception as e:
        logger.error(f"Failed to select the season year {year}: {e}")


# Function to attempt loading table data
def attempt_load_table(driver, dropdown, retries, category):
    for attempt in range(retries):
        try:
            # Check if 'View All' button is present
            view_all_buttons = driver.find_elements(By.CSS_SELECTOR, "div.np-mostrunsTab__btn.view-all a")
            if view_all_buttons:
                logging.info("Clicking 'View All' button using JavaScript to load the full table data.")
                driver.execute_script("arguments[0].click();", view_all_buttons[0])
                time.sleep(5)  # Wait for the full table data to load

                # Check if the table appears after clicking 'View All'
                tables = driver.find_elements(By.TAG_NAME, "table")
                if tables:
                    logging.info("Table found after clicking 'View All'.")
                    return True
                else:
                    logging.warning("No table found after clicking 'View All'. Retrying.")
            else:
                logging.info("No 'View All' button found, reselecting the category.")
                # Reclick the dropdown and reselect the category
                dropdown.click()
                time.sleep(1)
                dropdown.click()  # Click again to refresh
                time.sleep(2)
                # Re-select the category
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", category)
                    driver.execute_script("arguments[0].click();", category)
                    time.sleep(3)

                except Exception as e:
                    logger.error(f"Error clicking category: {category_name} in retry. Exception: {e}")

        except Exception as e:
            logging.error(f"Error attempting to load table data: {e}")
            continue

    return False


def scrape_stats_from_url(key, url):
    logger.info(f"Starting to scrape data from {url}")

    # Use Edge WebDriver with the correct initialization
    edge_driver_path = 'C:\\Users\\Harish Rajaram\\Downloads\\edgedriver_win64\\msedgedriver.exe'  # Change to your actual path
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service)

    try:
        # Open the target webpage
        logger.info(f"Opening the webpage: {url}")
        driver.get(url)

        # Wait for the dropdown to become visible
        wait = WebDriverWait(driver, 15)
        logger.info("Waiting for the dropdown to become visible.")

        # Select the desired season year from the dropdown
        select_season(driver, key)

        dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cSBDisplay')))

        # Click to open the dropdown menu
        logger.info("Clicking the dropdown menu to show categories.")
        dropdown.click()

        # Collect all category elements for both .batters and .bowlers
        logger.info("Collecting category elements for 'batters' and 'bowlers'.")
        categories_batters = driver.find_elements(By.CSS_SELECTOR, "div.cSBListItems.batters")
        categories_bowlers = driver.find_elements(By.CSS_SELECTOR, "div.cSBListItems.bowlers")
        categories = categories_batters + categories_bowlers

        category_data = {}

        # Iterate through each category option, click it, and extract the table data
        for category in categories:
            # Get the category name using get_attribute('innerText') to retrieve the dynamic text
            category_name = category.get_attribute('innerText')
            category_name = category_name.strip()
            logger.info(f"Scraping category: {category_name}")

            # Use JavaScript to ensure the element is clickable
            try:
                driver.execute_script("arguments[0].scrollIntoView();", category)
                driver.execute_script("arguments[0].click();", category)
            except Exception as e:
                logger.error(f"Error clicking category: {category_name}. Exception: {e}")

            time.sleep(3)  # Wait for the page to load the table data after clicking

            # Attempt to load the table data
            table_loaded = attempt_load_table(driver, dropdown, 3, category)

            if not table_loaded:
                logging.warning(f"Failed to load table data for category: {category_name} after 3 attempts.")
                continue

            # Scrape only the first table on the page
            logger.info("Scraping the first table on the page.")
            table = driver.find_elements(By.TAG_NAME, "table")[0]
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Extract table headers
            logger.info("Extracting table headers.")
            headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]

            # Extract table data
            data = []
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                try:
                    # Extract player name by skipping the image
                    logger.info(f"Extracting player name for row: {row}")
                    player_name = cells[1].find_element(By.CLASS_NAME, 'st-ply-name').text

                    # Collect other stats from the rest of the row (ignore the player image)
                    logger.info("Collecting the rest of the stats for the row.")
                    row_data = [cell.text for cell in cells]
                    row_data[1] = player_name  # Replace the player image and team with just the player's name
                    data.append(row_data)
                except Exception as e:
                    logger.error(f"Error processing row: {e}")

            # Store data in a DataFrame
            logger.info(f"Storing data for category: {category_name}")
            df = pd.DataFrame(data, columns=headers)
            category_data[category_name] = df

            # Reopen the category dropdown for the next category
            try:
                logger.info("Reopening the category dropdown menu.")
                dropdown.click()

                # Wait for the menu to become visible
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.cSBListItems")))

            except Exception as e:
                logger.error(f"Error reopening category dropdown: {e}")

    except Exception as e:
        logger.error(f"An error occurred while scraping {url}: {e}")
    finally:
        # Close the browser
        logger.info(f"Closing the browser after scraping data from {url}")
        driver.quit()

    logger.info(f"Finished scraping data from {url}")
    return category_data


# Function to write data to an Excel file
def write_data_to_excel(category_data, year):
    logger.info(f"Writing data to {year}_stats.xlsx")
    try:
        # Save all category data into an Excel file with each category as a separate sheet
        with pd.ExcelWriter(f'{year}_stats.xlsx') as writer:
            for category, df in category_data.items():
                logger.info(f"Writing data for category: {category} to sheet")
                df.to_excel(writer, sheet_name=category[:30], index=False)  # Sheet name limit of 31 characters
        logger.info(f"Data successfully written to {year}_stats.xlsx")
    except Exception as e:
        logger.error(f"Error writing to Excel for year {year}: {e}")


# Function to handle the entire process using the provided JSON
def scrape_data(file_path):
    logger.info(f"Starting the scraping process using URLs from {file_path}")
    try:
        # Load JSON containing the URLs from the file
        logger.info(f"Loading URLs from the JSON file: {file_path}")
        src = pd.read_json(file_path, typ='dictionary')

        # Iterate over each URL in the JSON
        for key, url in src.items():
            if key == "_comment":
                logger.info("Skipping comment in JSON file.")
                continue
            else:
                logger.info(f"Scraping data for year {key}")
                category_data = scrape_stats_from_url(key, url)
                write_data_to_excel(category_data, key)
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")


# Call the main function with the path to the JSON file
scrape_data('data.json')
