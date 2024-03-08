import re
import pandas as pd

from time import sleep     

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
from sqlalchemy import create_engine

# Database connection string
DATABASE_URL = "postgresql://myuser:mypassword@postgres_db:5432/mydatabase"

# Create a database engine
engine = create_engine(DATABASE_URL)


from selenium import webdriver
from bs4 import BeautifulSoup

def get_driver():
    options = webdriver.ChromeOptions()
    # Disable sharing memory across the instances
    options.add_argument('--disable-dev-shm-usage')
    # Initialize a remote WebDriver
    driver = webdriver.Remote(
            command_executor="http://hub:4444/wd/hub",
            options=options
        )
    return driver


def update_db(data, table_name='apartments_for_sale'):

    # Insert data into the database
    data.to_sql(table_name, engine, if_exists='append', index=True)


def get_apartment_data_from_element(tag):
    
    # Replace \xa0 symbols (non-breaking space) with regular spaces
    name = tag.find('span', attrs={'class': re.compile('name ng-binding')}).text.replace('\xa0', " ").split(" ")

    apartment_type = name[2]
    apartment_surface_area = name[3]

    
    location = tag.find('span', attrs={'class': re.compile('locality ng-binding')}).text.split(', ')

    street = location[0]

    try:
        city = location[1]
    except:
        city = location[0]

    
    price = tag.find('span', attrs={'class': re.compile('norm-price ng-binding')}).\
    text.replace('\xa0', " ").split(" ")[:-1]
    
    # Not all apartments have price available
    if price[0] == 'Info':
        price = None
    else:
        price = int("".join(price))

    
    return [apartment_type, apartment_surface_area, street, city, price]



def scrap_real_estate_source(entries=50):
    """
    Scrap the real estate
    """

    # Num of pages to scrap 20 is the default number of ads on the page
    page_num = entries//20 + 1

    # Restrict the number of possible pages to scrap
    page_limit = page_num*2
    
    browser = get_driver()

    entries_read = 0

    cur_page = 1
    while cur_page < page_num and page_num <= page_limit:
        print(f'Scraping page {cur_page}. Entries read: {entries_read}')
        url = f'https://www.sreality.cz/hledani/prodej/byty?strana={cur_page}&razeni=nejnovejsi'
        
        data_read = False

        for atempt in range(5):
            browser.get(url)
            soup = BeautifulSoup(browser.page_source, "html.parser")

            elements = soup.findAll('div', attrs={'class': re.compile("property ng-scope")})
            if len(elements) == 20:
                data_read = True
                break
            else:
                sec = 10
                sleep(sec)
                continue

        if not data_read:
            sec = 10
            print(f"PAGE {cur_page} failed. SKIPPING. SLEEPPING {sec} seconds")
            sleep(sec)
            cur_page += 1
            page_num += 1
            continue

        records = []   

        for element in elements:    
            records.append(get_apartment_data_from_element(element)) 

        data = pd.DataFrame(records, columns=['type', 'surface_area', 'street', 'city', 'price'])
        print(data)
        if data.shape[0] > 0:
            update_db(data)
            print(f"Data from page {cur_page} added to db\n\n")
            entries_read += data.shape[0]
        else:
            print(f"PARSING OF PAGE {cur_page} FAILED")
        
        cur_page += 1
        sleep(2)
    browser.close()
    browser.quit()


if __name__ == '__main__':
    print("SCRAP APP: START")
    scrap_real_estate_source()
    print("SCRAP APP: FINISH")