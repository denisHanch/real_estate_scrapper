from sqlalchemy import create_engine
import pandas as pd

# Database connection string
DATABASE_URL = "postgresql://myuser:mypassword@postgres_db:5432/mydatabase"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Function to import data from CSV into the database
def import_data(csv_file, table_name):
    # Read CSV file
    df = pd.read_csv(csv_file)
    # Insert data into the database
    df.to_sql(table_name, engine, if_exists='append', index=False)

# Import data from CSV files
import_data('customers.csv', 'customers')
import_data('orders.csv', 'orders')
