import streamlit as st
import pandas as pd
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Get credentials
username = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')

# Database connection
DATABASE_URL = f"postgresql://{username}:{password}@postgres_db:5432/{database}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def load_data():
    # Perform query.
    session = Session()
    apartments = session.execute(text("SELECT * FROM apartments_for_sale")).fetchall()
    return pd.DataFrame(apartments)

def main():
    st.title('Czech Republic real estate data')

    data = load_data()

    st.write(data)

if __name__ == "__main__":
    main()
