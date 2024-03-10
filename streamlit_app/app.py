import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
    # Query the db
    session = Session()
    apartments = session.execute(text("SELECT * FROM apartments_for_sale")).fetchall()
    
    return pd.DataFrame(apartments)

def main():
    st.title('Czech Republic real estate data')

    data = load_data()
    data.drop('id', axis=1, inplace=True)
    st.write(data)

    trunc_outliers = st.sidebar.radio('Truncate outliers?', 
                                      ['Yes', 'No'], 
                                      index=1)
    # Add separation
    st.sidebar.markdown("---")
    

    column_to_plot = st.sidebar.radio('Choose a column for the X-axis:', 
                                      ['price', 'apt_size_m_sqrt'], 
                                      index=0)
    # Add separation
    st.sidebar.markdown("---")
    
    # Remove outliers
    if trunc_outliers == 'Yes':
        q2 = np.quantile(data[column_to_plot], .25)
        q3 = np.quantile(data[column_to_plot], .75)
        iqr = q3 - q2
        upper_bound = q3 + 1.5 * iqr
        data = data[data[column_to_plot] < upper_bound].reset_index(drop=True).copy()


    apt_types = st.sidebar.radio("Select apartment type:", ['All types', 'Subset'], index=0)
    if apt_types == 'Subset':

        cat_list = data['apt_type'].unique()
        val = [None]* len(cat_list) 
        for i, cat in enumerate(cat_list):
            # create a checkbox for each category
            val[i] = st.sidebar.checkbox(cat)

        # filter data based on selection
        data = data[data['apt_type'].isin(cat_list[val])].reset_index(drop=True).copy()
        if data.shape[0] == 0:
            st.write("No categories selected")
            return

    # Curated labels for histplot
    xlabs = { 'price': 'Price (Kč)', 
             'apt_size_m_sqrt': 'Apartment size m2'
            }
    #Plot data
    g = sns.histplot(data=data, x=column_to_plot, hue='apt_type', kde=True)

    plt.xlabel(xlabs[column_to_plot])
    plt.ylabel('Frequency')
    
    # Display the plot in Streamlit
    st.pyplot(g.figure)

if __name__ == "__main__":
    main()
