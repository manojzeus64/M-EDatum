import pandas as pd
import streamlit as st


@st.cache_data
def load_data(filename):
    return pd.read_csv(filename)


@st.cache_data
def get_summary_stats(data):
    return data.describe()


@st.cache_data
def prepare_data(data):
    # Process Columns
    data[['order_day', 'order_month', 'order_year']] = data['Order Date'].str.split('-', expand=True)
    data['Order Date'] = data['order_year'] + '/' + data['order_month'] + '/' + data['order_day']
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data[['ship_day', 'ship_month', 'ship_year']] = data['Ship Date'].str.split('-', expand=True)
    data['Ship Date'] = data['ship_year'] + '/' + data['ship_month'] + '/' + data['ship_day']
    data['Ship Date'] = pd.to_datetime(data['Ship Date'])
    data['Ship Mode'] = data['Ship Mode'].astype('category')
    data['Segment'] = data['Segment'].astype('category')
    data['Country'] = data['Country'].astype('category')
    data['Market'] = data['Market'].astype('category')
    data['Region'] = data['Region'].astype('category')
    data['Category'] = data['Category'].astype('category')
    data['Sub-Category'] = data['Sub-Category'].astype('category')
    data['Order Priority'] = data['Order Priority'].astype('category')

    # Drop Unwanted Columns
    data.drop(columns=['order_day', 'order_month', 'order_year', 'ship_day'], inplace=True)
    data.drop(columns=['ship_month', 'ship_year', 'Unnamed: 0'], inplace=True)

    return data


@st.cache_data
def remove_spaces(data):
    for cols in data.columns:
        if data[cols].dtypes in ['object', 'category']:
            data[cols] = data[cols].str.strip()
        return data
