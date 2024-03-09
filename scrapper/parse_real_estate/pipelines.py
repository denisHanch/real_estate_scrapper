# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2


class ParseRealEstatePipeline:
     
    def __init__(self):
        ## Connection Details
        hostname = 'postgres_db'
        username = 'myuser'
        password = 'mypassword' # your password
        database = 'mydatabase'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS apartments_for_sale(
            id serial PRIMARY KEY, 
            name text,
            locality text,
            price INT
        )
        """)
        
    
    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into apartments_for_sale (name, locality, price) values (%s,%s,%s)""", (
            item["name"],
            item["locality"],
            item["price"]
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
