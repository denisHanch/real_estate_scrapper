import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

print("APP START")

# Database connection
DATABASE_URL = "postgresql://myuser:mypassword@postgres_db:5432/mydatabase"
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
