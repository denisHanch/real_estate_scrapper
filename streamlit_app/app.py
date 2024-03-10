import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
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
    data.drop('id', axis=1, inplace=True)
    st.write(data)

    column_to_plot = st.sidebar.radio('Choose a column for the X-axis:', 
                                      ['price', 'apt_size_m_sqrt'], 
                                      index=0)
    #Plot data
    g = sns.histplot(data=data, x=column_to_plot, hue='apt_type', kde=True)
    plt.xlabel(column_to_plot.capitalize())
    plt.ylabel('Frequency')


    
    # Display the plot in Streamlit
    st.pyplot(g.figure)

if __name__ == "__main__":
    main()
