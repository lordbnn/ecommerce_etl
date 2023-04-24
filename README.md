# E-COMMERCE DATA PIPELINE WITH AIRFLOW
This is an ETL data pipeline for an e-commerce website that involves web scraping, data transformation, and loading the transformed data into a PostgreSQL database. The pipeline is built using Apache Airflow, an open-source platform to programmatically author, schedule, and monitor workflows.

## INSTALLATION

### Clone the repository:
git clone https://github.com/lordbnn/ecommerce_etl.git

### Install the required packages:
pip install -r requirements.txt

## USAGE
- Set up a PostgreSQL database to store the scraped data.

- Update the database credentials in the ecommerce_etl.py file.

- Update the Airflow configuration in the airflow.cfg file to reflect your environment.

- Start the Airflow web server and scheduler:

  - airflow webserver -p 8080
  - airflow scheduler
  - Access the Airflow web UI at http://localhost:8080/ and turn on the ecommerce_webscraping DAG.

## ETL PIPELINE
The pipeline consists of three tasks: scrape_data, clean_data, and load_data.

### Scrape Data
The scrape_data task calls the scrape_jumia function from the ecommerce_etl module to scrape data from the Jumia e-commerce website and save the results to a JSON file.

### Clean Data
The clean_data task calls the clean_data function from the ecommerce_etl module to clean the scraped data and remove any duplicates or irrelevant information.

### Load Data
The load_data task calls the load_json_to_postgres function from the ecommerce_etl module to load the cleaned data into a PostgreSQL database.

## DAG
The pipeline is orchestrated using an Airflow DAG, defined in ecommerce_dag.py. The DAG is scheduled to run daily, and the tasks are dependent on each other, with scrape_data running first, followed by clean_data, and finally load_data.
