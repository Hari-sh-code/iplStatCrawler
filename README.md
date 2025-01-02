# IPL Stats Scraper

A Python-based project that scrapes IPL player statistics from a website, stores the data in an Excel file, and displays it using a Tkinter-based GUI.

## Features

- Scrapes IPL player statistics from a website using Selenium.
- Stores the scraped data in an Excel file for easy access.
- Displays the data in a user-friendly Tkinter GUI interface.
- Allows users to filter, search, and display player statistics.

## Requirements

Before running this project, make sure you have the following installed:

- Python 3.12 or higher
- Selenium
- Tkinter (comes pre-installed with Python)
- Pandas
- openpyxl (for Excel file handling)

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/ipl-stats-scraper.git
```
2. Navigate to the project folder:
```
cd ipl-stats-scraper
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Navigate to the user interface directory:
```
cd uiModule
```
5. Run the python script
```
python main.py
```

The GUI will appear, allowing you to select the IPL year and categories, and display player statistics.

## Project Structure
```
ipl-stats-scraper/
│
├── main.py             # Main script to run the application
├── requirements.txt    # List of required dependencies
├── README.md           # Project documentation
├── drivers/            # Folder containing browser drivers (e.g., ChromeDriver)
└── data/               # Folder for storing scraped data (Excel files)
```
## Functions

Web Scraping:
- The scraper uses Selenium to fetch IPL player data from a live website.
- Data is stored in an Excel file for later use.

GUI Interface:
- Built using Tkinter, the GUI allows users to interact with the scraped data.
- Features include selecting categories, searching for players, and viewing data.
