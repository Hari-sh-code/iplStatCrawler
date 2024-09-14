import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup logging
logging.basicConfig(
    filename='test1.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to scrape stats from the URL
def scrape_stats_from_url(url):
    logging.info(f"Starting to scrape data from {url}")

    # Set up the ChromeDriver service
    service = ChromeService(executable_path='/usr/local/bin/chromedriver')  # Path to ChromeDriver

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Path to Chromium binary
    chrome_options.headless = False  # Set to True if you want to run Chromium in headless mode

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the target webpage
        logging.info(f"Opening the webpage: {url}")
        driver.get(url)

        # Wait for the dropdown to become visible
        wait = WebDriverWait(driver, 10)
        logging.info("Waiting for the dropdown to become visible.")
        dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cSBDisplay')))

        # Click to open the dropdown menu
        logging.info("Clicking the dropdown menu to show categories.")
        dropdown.click()

        # Collect all category elements for both .batters and .bowlers
        logging.info("Collecting category elements for 'batters' and 'bowlers'.")
        categories_batters = driver.find_elements(By.CSS_SELECTOR, "div.cSBListItems.batters")
        categories_bowlers = driver.find_elements(By.CSS_SELECTOR, "div.cSBListItems.bowlers")
        categories = categories_batters + categories_bowlers

        category_data = {}

        # Iterate through each category option, click it, and extract the table data
        for category in categories:
            category_name = category.text
            logging.info(f"Scraping category: {category_name}")
            category.click()
            time.sleep(3)  # Wait for the page to load the table data after clicking

            # Scrape only the first table on the page
            logging.info("Scraping the first table on the page.")
            table = driver.find_elements(By.TAG_NAME, "table")[0]
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Extract table headers
            logging.info("Extracting table headers.")
            headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]

            # Extract table data
            data = []
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                try:
                    # Extract player name by skipping the image
                    logging.info(f"Extracting player name for row: {row}")
                    player_name = cells[1].find_element(By.CLASS_NAME, 'st-ply-name').text

                    # Collect other stats from the rest of the row (ignore the player image)
                    logging.info("Collecting the rest of the stats for the row.")
                    row_data = [cell.text for cell in cells]
                    row_data[1] = player_name  # Replace the player image and team with just the player's name
                    data.append(row_data)
                except Exception as e:
                    logging.error(f"Error processing row: {e}")

            # Store data in a DataFrame
            logging.info(f"Storing data for category: {category_name}")
            df = pd.DataFrame(data, columns=headers)
            category_data[category_name] = df

            # Open the dropdown again for the next category selection
            logging.info("Opening the dropdown again for the next category.")
            dropdown.click()

    except Exception as e:
        logging.error(f"An error occurred while scraping {url}: {e}")
    finally:
        # Close the browser
        logging.info(f"Closing the browser after scraping data from {url}")
        driver.quit()

    logging.info(f"Finished scraping data from {url}")
    return category_data

# Function to write data to an Excel file
def write_data_to_excel(category_data, year):
    logging.info(f"Writing data to {year}_stats.xlsx")
    try:
        # Save all category data into an Excel file with each category as a separate sheet
        with pd.ExcelWriter(f'{year}_stats.xlsx') as writer:
            for category, df in category_data.items():
                logging.info(f"Writing data for category: {category} to sheet")
                df.to_excel(writer, sheet_name=category[:30], index=False)  # Sheet name limit of 31 characters
        logging.info(f"Data successfully written to {year}_stats.xlsx")
    except Exception as e:
        logging.error(f"Error writing to Excel for year {year}: {e}")

# Function to handle the entire process using the provided JSON
def scrape_data(file_path):
    logging.info(f"Starting the scraping process using URLs from {file_path}")
    try:
        # Load JSON containing the URLs from the file
        logging.info(f"Loading URLs from the JSON file: {file_path}")
        src = pd.read_json(file_path, typ='dictionary')

        # Iterate over each URL in the JSON
        for key, url in src.items():
            if key == "_comment":
                logging.info("Skipping comment in JSON file.")
                continue
            else:
                logging.info(f"Scraping data for year {key}")
                category_data = scrape_stats_from_url(url)
                write_data_to_excel(category_data, key)
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

# Call the main function with the path to the JSON file
scrape_data('data.json')