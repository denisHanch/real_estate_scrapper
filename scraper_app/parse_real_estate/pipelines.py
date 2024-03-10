# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import psycopg2


class ParseRealEstatePipeline:
     
    def __init__(self):
        ## Get credentials
        hostname = 'postgres_db'
        username = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        database = os.getenv('POSTGRES_DB')

        ## Create connection to db
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor
        self.cur = self.connection.cursor()
        
        ## Create table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS apartments_for_sale(
            id serial PRIMARY KEY, 
            name text,
            locality text,
            price INT,
            apt_type text,
            apt_size_m_sqrt INT,
            street text,
            city text
        )
        """)
        
    
    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into apartments_for_sale (name, locality, price, apt_type, apt_size_m_sqrt, street, city) values (%s,%s,%s,%s,%s,%s,%s)""", (
            item["name"],
            item["locality"],
            item["price"],
            item['apt_type'],
            item['apt_size_m_sqrt'],
            item['street'],
            item['city']
        ))

        ## Insert of data into DB
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Clean up
        self.cur.close()
        self.connection.close()
