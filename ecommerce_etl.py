
#MULTIPLE PAGES

#File format required
import json

#Webscraping tools
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

#For connection to Postgres_db
import psycopg2
from psycopg2 import extras
 
   
   
  #SINGLE PAGE SCRAPING
def scrape_jumia():
    # Define the search URL
    url = 'https://www.jumia.com.ng/all-products/'

    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Navigate to the search results page
    driver.get(url)
    time.sleep(5)  # Wait for page to load
    #print(driver.page_source)

    # Extract product details
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    products = []
    for product in soup.find('div', class_='-paxs row _no-g _4cl-3cm-shs'):
        product_dict = {}
        item_name = product.find('h3', class_='name')
        if item_name is not None:
            product_dict['product'] = item_name.text.strip()
        else:
            product_dict['product'] = ''
        product_brand = product.find('a', {'class': 'core'})
        if product_brand is not None:
            product_dict['brand'] = product_brand['data-brand']
        else:
            product_dict['brand'] = ''            
        product_category = product.find('a', {'class': 'core'})
        if product_category is not None:
            product_dict['category'] = product_category['data-category']
        else:
            product_dict['category'] = ''
        product_price = product.find('div', class_='prc')
        if product_price is not None:
            product_price= product_price.text.strip()
            #Remove the Naira symbols
            product_dict['price'] = product_price.replace('\u20a6', '').replace(',', '').strip()
        else:
            product_dict['price'] = ''
        rating = product.find('div', class_='stars _s')
        if rating is not None:
            product_dict['ratings'] = rating.text.strip().split(' ')[0]
        else:
            product_dict['ratings'] = ''
            
        item_reviews = product.find('div', class_='rev')
        if rating is not None:
            product_dict['reviews'] = item_reviews.text.split('(')[-1].replace(')',' ').strip()
        else:
            product_dict['reviews'] = '' 
            
            
        # Add any other relevant details here
        products.append(product_dict)
        
    # Close the browser
    driver.quit()

    # Output the result as JSON
    return json.dumps(products)


    
    
    
#CLEAN & TRANSFORM (Duplicates, average price for range, etc)

def clean_data(data):
    cleaned_data = []
    seen_products = set()
    for item in data:
        if item['product'] and item['brand']:
            key = (item['product'], item['category'])
            if key in seen_products:
                # Skip duplicates
                continue
            else:
                seen_products.add(key)

            cleaned_item = {}
            cleaned_item['product'] = item['product']
            cleaned_item['brand'] = item['brand']
            if item['category'] == 'computing':
                cleaned_item['category'] = 'Computers & Accessories'
            elif item['category'] == 'televisions':
                cleaned_item['category'] = 'TVs'
            else:
                cleaned_item['category'] = item['category'].capitalize()

            if '-' not in item['price']:
                cleaned_item['price'] = float(item['price'])
            else:
                ranged_price= item['price'].split('-')
                cleaned_item['price'] = (float(ranged_price[0]) + float(ranged_price[-1]))/2 

            if item['ratings']:
                cleaned_item['ratings'] = float(item['ratings'])
            else:
                cleaned_item['ratings'] = 0
            if item['reviews']:
                cleaned_item['reviews'] = int(item['reviews'])
            else:
                cleaned_item['reviews'] = 0
            cleaned_data.append(cleaned_item)
    return cleaned_data




# POSTGRES CONNECTION

def create_server_connection():    
    connection = None
    try:

        connection = psycopg2.connect(
            database='d2b_assessment',
            user='byroneji4734',
            password='npF5SlOzvW',
            host='d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com',
            port='5432'
        )
        
        print("PostgreSql Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection





# DIRECTLY LOAD JSON INTO POSTGRES AND SKIP DUPLICATES

def load_json_to_postgres(json_data):
    

    conn = psycopg2.connect(
        database='d2b_assessment',
        user='byroneji4734',
        password='npF5SlOzvW',
        host='d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com',
        port='5432')

    
    clean_json = json.dumps(json_data)
    # Parse the JSON data
    data = json.loads(clean_json)

    # Convert any NaN values to None
    data = [{k: v if v is not None else None for k, v in row.items()} for row in data]

    # Create a list of dictionaries from the JSON data
    rows = [tuple(row.values()) for row in data]
    cols = list(data[0].keys())

    # Create the SQL query to create the table if it does not exist
    create_query = f"""CREATE TABLE IF NOT EXISTS public.ecommerce (
                      product varchar,
                      brand varchar,
                      category varchar,
                      price float,
                      ratings float,
                      reviews int,
                      PRIMARY KEY(product,category)
                        )"""

    cursor = conn.cursor()
    cursor.execute(create_query)
    conn.commit()

    # Create the SQL query to insert the data into the table with "ON CONFLICT" statement
    insert_query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT DO NOTHING" % (table, ','.join(cols))
    #print(insert_query)

    # Execute the SQL query
    try:
        extras.execute_values(cursor, insert_query, rows)
        conn.commit()
        print("Data inserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    finally:
        cursor.close()

    