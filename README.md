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
├── README.md
├── uiModule
    ├── data_management
    │   ├── __init__.py
    │   ├── list_categories.py
    │   ├── load_category_data.py
    │   └── validate_excel_files.py
    ├── main.py
    ├── player
    │   ├── __init__.py
    │   ├── collect_player_stats.py
    │   └── suggest_player_names.py
    └── requirements.txt
└── scrapeModule
    ├── data.json
    ├── outputLog.log
    ├── requirements.txt
    ├── scrape.py
    └── statsData
        ├── 2008_stats.xlsx
        ├── 2009_stats.xlsx
        ├── 2010_stats.xlsx
        ├── 2011_stats.xlsx
        ├── 2012_stats.xlsx
        ├── 2013_stats.xlsx
        ├── 2014_stats.xlsx
        ├── 2015_stats.xlsx
        ├── 2016_stats.xlsx
        ├── 2017_stats.xlsx
        ├── 2018_stats.xlsx
        ├── 2019_stats.xlsx
        ├── 2020_stats.xlsx
        ├── 2021_stats.xlsx
        ├── 2022_stats.xlsx
        ├── 2023_stats.xlsx
        └── 2024_stats.xlsx
```
## Functions

Web Scraping:
- The scraper uses Selenium to fetch IPL player data from a live website.
- Data is stored in an Excel file for later use.

GUI Interface:
- Built using Tkinter, the GUI allows users to interact with the scraped data.
- Features include selecting categories, searching for players, and viewing data.
