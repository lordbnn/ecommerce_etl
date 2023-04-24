# E-COMMERCE DATA PIPELINE WITH AIRFLOW
This is an ETL data pipeline for an e-commerce website that involves web scraping, data transformation, and loading the transformed data into a PostgreSQL database. The pipeline is built using Apache Airflow, an open-source platform to programmatically author, schedule, and monitor workflows.

## INSTALLATION

### Clone the repository:
git clone https://github.com/lordbnn/ecommerce_etl.git

### Install the required packages:
To run this code, you need to have the following software installed on your machine:

  - Python 3.x
  - Chrome browser (for Selenium to work)

  In addition, you need to install the following Python libraries:

  - json
  - BeautifulSoup
  - selenium
  - webdriver_manager
  - psycopg2

## USAGE
- Set up a PostgreSQL database to store the scraped data.

- Update the database credentials in the ecommerce_etl.py file.

- Update the Airflow configuration in the airflow.cfg file to reflect your environment.

- Start the Airflow web server and scheduler:

  - airflow webserver -p 8080
  - airflow scheduler
  - Access the Airflow web UI at http://localhost:8080/ and turn on the ecommerce_webscraping DAG.

## ETL PIPELINE
This repository contains code for web scraping data from multiple pages of an e-commerce website, cleaning and transforming the data, and loading the data into a Postgres database. The code is written in Python and uses the following libraries:

  - json for handling JSON data
  - BeautifulSoup for parsing HTML
  - selenium for automating web browsing
  - webdriver_manager for managing web drivers
  - psycopg2 for connecting to and working with Postgres databases

### Scrape Data
The scrape_data task calls the scrape_jumia function from the ecommerce_etl module to scrape data from the Jumia e-commerce website and save the results to a JSON file.

### Clean Data
The clean_data task calls the clean_data function from the ecommerce_etl module to clean the scraped data and removes irrelevant information.
This module takes the JSON data as input, cleans it by removing duplicates and transforming certain fields (e.g. converting the price range to the average price), and returns the cleaned data as a list of dictionaries.

### Load Data
The load_data task calls the load_json_to_postgres function from the ecommerce_etl module to load the cleaned data into a PostgreSQL database.
This function loads the cleaned data directly into a PostgreSQL database. It connects to the database, creates a table if it does not exist, and inserts the data into the table with an "ON CONFLICT" statement to avoid duplicate entries.

## DAG
The pipeline is orchestrated using an Airflow DAG, defined in ecommerce_dag.py. The DAG is scheduled to run daily, and the tasks are dependent on each other, with scrape_data running first, followed by clean_data, and finally load_data.
