import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import os

# Setup custom logger
logger = logging.getLogger('web_scraper')
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('test6.log')
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)


def handle_cookies(driver):
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='cookie__accept']"))
        )
        cookie_button.click()
        logger.info("Accepted cookie message.")
    except Exception as e:
        logger.info("No cookie message to handle.")


def select_season(driver, year):
    try:
        logger.info("Attempting to open the season dropdown menu.")
        season_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.customSelecBox div.cSBDisplay"))
        )
        driver.execute_script("arguments[0].click();", season_dropdown)
        logger.info(f"Looking for the season year: {year}")
        season_year_option = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f"div.cSBListItems[data-val='{year}']"))
        )
        logger.info(f"Clicking the season year: {year}")
        driver.execute_script("arguments[0].click();", season_year_option)
        logger.info(f"Successfully selected season year {year}.")
    except Exception as e:
        logger.error(f"Failed to select the season year {year}: {e}")


def attempt_load_table(driver, dropdown, retries, category):
    for attempt in range(retries):
        try:
            view_all_buttons = driver.find_elements(By.CSS_SELECTOR, "div.np-mostrunsTab__btn.view-all a")
            if view_all_buttons:
                logger.info("Clicking 'View All' button using JavaScript to load the full table data.")
                driver.execute_script("arguments[0].click();", view_all_buttons[0])
                time.sleep(5)
                tables = driver.find_elements(By.TAG_NAME, "table")
                if tables:
                    logger.info("Table found after clicking 'View All'.")
                    return True
                else:
                    logger.warning("No table found after clicking 'View All'. Retrying.")
            else:
                logger.info("No 'View All' button found, reselecting the category.")
                dropdown.click()
                time.sleep(1)
                dropdown.click()
                time.sleep(2)
                driver.execute_script("arguments[0].scrollIntoView();", category)
                driver.execute_script("arguments[0].click();", category)
                time.sleep(3)
        except Exception as e:
            logger.error(f"Error attempting to load table data: {e}")
            continue
    return False


def scrape_stats_from_url(key, url):
    logger.info(f"Starting to scrape data from {url}")
    edge_driver_path = 'C:\\Users\\Harish Rajaram\\Downloads\\edgedriver_win64\\msedgedriver.exe'
    service = Service(executable_path=edge_driver_path)
    driver = webdriver.Edge(service=service)

    try:
        logger.info(f"Opening the webpage: {url}")
        driver.get(url)
        handle_cookies(driver)
        wait = WebDriverWait(driver, 15)
        logger.info("Waiting for the dropdown to become visible.")
        select_season(driver, key)
        dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'cSBDisplay')))
        logger.info("Clicking the dropdown menu to show categories.")
        dropdown.click()
        logger.info("Collecting category elements for 'batters' and 'bowlers'.")
        categories_batters = driver.find_elements(By.CSS_SELECTOR, "div.cSBListItems.batters")
        categories_bowlers = driver.find_elements(By.CSS_SELECTOR, "div.cSBListItems.bowlers")
        categories = categories_batters + categories_bowlers

        category_data = {}

        for category in categories:
            category_name = category.get_attribute('innerText').strip()
            logger.info(f"Scraping category: {category_name}")
            try:
                driver.execute_script("arguments[0].scrollIntoView();", category)
                driver.execute_script("arguments[0].click();", category)
            except Exception as e:
                logger.error(f"Error clicking category: {category_name}. Exception: {e}")

            time.sleep(3)
            table_loaded = attempt_load_table(driver, dropdown, 3, category)
            if not table_loaded:
                logger.warning(f"Failed to load table data for category: {category_name} after 3 attempts.")
                continue

            logger.info("Scraping the first table on the page.")
            table = driver.find_elements(By.TAG_NAME, "table")[0]
            rows = table.find_elements(By.TAG_NAME, "tr")

            logger.info("Extracting table headers.")
            headers = [header.text for header in rows[0].find_elements(By.TAG_NAME, "th")]

            data = []
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                try:
                    logger.info(f"Extracting player name for row: {row}")
                    player_name = cells[1].find_element(By.CLASS_NAME, 'st-ply-name').text
                    logger.info("Collecting the rest of the stats for the row.")
                    row_data = [cell.text for cell in cells]
                    row_data[1] = player_name
                    data.append(row_data)
                except Exception as e:
                    logger.error(f"Error processing row: {e}")

            logger.info(f"Storing data for category: {category_name}")
            df = pd.DataFrame(data, columns=headers)
            category_data[category_name] = df

            try:
                logger.info("Reopening the category dropdown menu.")
                dropdown.click()
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.cSBListItems")))
            except Exception as e:
                logger.error(f"Error reopening category dropdown: {e}")

    except Exception as e:
        logger.error(f"An error occurred while scraping {url}: {e}")
    finally:
        logger.info(f"Closing the browser after scraping data from {url}")
        driver.quit()

    logger.info(f"Finished scraping data from {url}")
    return category_data


def write_data_to_excel(category_data, year):
    logger.info(f"Writing data to {year}_stats.xlsx")
    try:
        # Ensure the statsData directory exists
        output_directory = './statsData'
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, f'{year}_stats.xlsx')

        with pd.ExcelWriter(output_path) as writer:
            for category, df in category_data.items():
                logger.info(f"Writing data for category: {category} to sheet")
                df.to_excel(writer, sheet_name=category[:30], index=False)
        logger.info(f"Data successfully written to {output_path}")
    except Exception as e:
        logger.error(f"Error writing to Excel for year {year}: {e}")


def scrape_data(file_path):
    logger.info(f"Starting the scraping process using URLs from {file_path}")
    try:
        logger.info(f"Loading URLs from the JSON file: {file_path}")
        src = pd.read_json(file_path, typ='dictionary')
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

scrape_data('data.json')