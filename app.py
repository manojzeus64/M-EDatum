import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import datetime as dt
import json
import streamlit as st

data = pd.read_csv('superstore.csv')
data[['order_day', 'order_month', 'order_year']] = data['Order Date'].str.split('-', expand=True)
data['Order Date'] = data['order_year'] + '/' + data['order_month'] + '/' + data['order_day']
data['Order Date'] = pd.to_datetime(data['Order Date'])
data[['ship_day', 'ship_month', 'ship_year']] = data['Ship Date'].str.split('-', expand=True)
data['Ship Date'] = data['ship_year'] + '/' + data['ship_month'] + '/' + data['ship_day']
data['Ship Date'] = pd.to_datetime(data['Ship Date'])
data.drop(columns=['order_day', 'order_month', 'order_year', 'ship_day', 'ship_month', 'ship_year', 'Unnamed: 0'], inplace=True)
data['Ship Mode'] = data['Ship Mode'].astype('category')
data['Segment'] = data['Segment'].astype('category')
data['Country'] = data['Country'].astype('category')
data['Market'] = data['Market'].astype('category')
data['Region'] = data['Region'].astype('category')
data['Category'] = data['Category'].astype('category')
data['Sub-Category'] = data['Sub-Category'].astype('category')
data['Order Priority'] = data['Order Priority'].astype('category')


def removeSpaces(df):
    for cols in df.columns:
        if df[cols].dtypes in ['object', 'category']:
            df[cols] = df[cols].str.strip()
        return df


data = removeSpaces(data)
st.set_page_config(page_title="SAMACHARA DRUSHYA")
st.title('EDATUM SAMACHARA DRUSHYA')


def mainPage():
    st.sidebar.markdown("# EDATUM 🎈")
    st.subheader('Super Store Dataset')
    st.dataframe(data)
    st.subheader('Numerical Statistics')
    st.dataframe(data.describe())


def page2():
    st.sidebar.markdown("# SAMACHARAM 1 ❄️")
    country_group = data.groupby('Country')
    country_sales = country_group.agg({'Sales': 'sum'})
    country_sales.sort_values(by='Sales', ascending=False)
    top_7 = country_sales.nlargest(7, 'Sales')
    top_7.reset_index()

    st.markdown("## Top 7 Countries Vs Total Sales")
    fig = plt.figure(figsize=(5, 8))
    explode = [0.08, 0, 0, 0, 0, 0, 0]
    plt.pie(top_7['Sales'], labels=list(top_7.index), explode=explode, shadow=True,
            startangle=90, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
    st.pyplot(fig)

    st.markdown("## Segment Of Customers VS Profit")
    custSeg = data.groupby('Segment')
    df = custSeg.aggregate({'Profit': 'sum'})
    df.reset_index(inplace=True)
    fig = plt.figure(figsize=(5, 8))
    names = df['Segment'].values
    marks = df['Profit'].values
    my_circle = plt.Circle((0, 0), 0.45, color='white')
    plt.pie(marks, labels=names, autopct='%1.1f%%', colors=['red', 'green', 'blue']
            , wedgeprops={'edgecolor': 'black'}, startangle=90)
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    st.pyplot(fig)

    st.markdown("## Top 5 Profit-Making Product Types")
    year_category_group = data.groupby(['order year', 'Sub-Category'])
    year_category_profit_df = year_category_group.agg({'Profit': 'sum'})
    year_category_profit_df.reset_index(inplace=True)
    category_yearly_profit = year_category_profit_df.groupby('order year')
    top5_profit_category = pd.DataFrame(columns=year_category_profit_df.columns)

    for g, d in category_yearly_profit:
        high_profit_categories = d.nlargest(5, 'Profit')
        top5_profit_category = pd.concat([top5_profit_category, high_profit_categories])

    fig = plt.figure(figsize=(14, 11))
    plt.subplot(2, 2, 1)
    x = list(top5_profit_category[top5_profit_category['order year'] == 2012]['Sub-Category'])
    y = top5_profit_category[top5_profit_category['order year'] == 2012]['Profit']
    sns.barplot(x=x, y=y, palette='husl')
    plt.title("Year-2012")

    plt.subplot(2, 2, 2)
    x = list(top5_profit_category[top5_profit_category['order year'] == 2013]['Sub-Category'])
    y = top5_profit_category[top5_profit_category['order year'] == 2013]['Profit']
    sns.barplot(x=x, y=y, palette='Paired')
    plt.title("Year-2013")

    plt.subplot(2, 2, 3)
    x = list(top5_profit_category[top5_profit_category['order year'] == 2014]['Sub-Category'])
    y = top5_profit_category[top5_profit_category['order year'] == 2014]['Profit']
    sns.barplot(x=x, y=y)
    plt.title("Year-2014")

    plt.subplot(2, 2, 4)
    x = list(top5_profit_category[top5_profit_category['order year'] == 2015]['Sub-Category'])
    y = top5_profit_category[top5_profit_category['order year'] == 2015]['Profit']
    sns.barplot(x=x, y=y, palette='hls')
    plt.title("Year-2015")
    st.pyplot(fig)

    st.markdown("## Delivery Speeds Of Top 20 Countries")
    top_20_sales = country_sales.nlargest(20, 'Sales')
    data['Delivery Duration'] = data['Ship Date'] - data['Order Date']
    country_group = data.groupby('Country')
    delivery_duration_df = country_group.agg({'Delivery Duration': 'mean'})
    delivery_duration_df['Duration In Hours'] = delivery_duration_df['Delivery Duration'] / dt.timedelta(hours=1)
    top20_sales_country_DD = top_20_sales.merge(delivery_duration_df, how='left', left_index=True, right_index=True)
    top20_sales_country_DD.reset_index(inplace=True)
    top20_sales_country_DD.sort_values(by='Duration In Hours')
    labels = []
    for time in list(top20_sales_country_DD['Duration In Hours']):
        if 83 <= time <= 94:
            labels.append('Fast')
        elif 94 <= time <= 99:
            labels.append('Average')
        else:
            labels.append('Slow')
    fig = plt.figure(figsize=(10, 5))
    x = list(top20_sales_country_DD['Country'])
    y = list(top20_sales_country_DD['Duration In Hours'])
    sns.scatterplot(x=x, y=y, s=80, hue=labels, palette='Dark2')
    plt.legend(loc='upper left')
    plt.xticks(rotation=90)
    st.pyplot(fig)


def page3():
    st.sidebar.markdown("# SAMACHARAM 2 🎉")
    st.markdown("## Profit Vs Month")
    df_month = data.groupby(['order month', 'order year'])
    df_pro = df_month.aggregate({'Profit': 'sum'})
    df_sal = df_month.aggregate({'Sales': 'sum'})
    df_pro.reset_index(inplace=True)
    df_sal.reset_index(inplace=True)
    df = df_pro.merge(df_sal)
    df['month'] = df['order month'].map(
        {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
         8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    fig = px.line(df, x="month", y="Profit", color='order year', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## Countries VS Sales")
    with open('iso_mapping.json', 'r') as json_file:
        iso_mapping = json.load(json_file)
    print(iso_mapping)
    country_group = data.groupby('Country')
    country_sales = country_group.agg({'Sales': 'sum'})
    df = country_sales.reset_index()
    df['ISO Code'] = df['Country'].map(iso_mapping)
    fig = px.choropleth(df, locations="ISO Code",
                        color="Sales",
                        hover_name="Country",
                        color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)


page_names_to_funcs = {
    "EDATUM": mainPage,
    "SAMACHARAM 1": page2,
    "SAMACHARAM 2": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
