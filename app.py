import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import datetime as dt
import streamlit as st


data = pd.read_csv('superstore.csv')
data[['order_day','order_month','order_year']] = data['Order Date'].str.split('-', expand=True)
data['Order Date'] = data['order_year'] + '/' + data['order_month'] + '/' + data['order_day']
data['Order Date'] = pd.to_datetime(data['Order Date'])
data[['ship_day','ship_month','ship_year']] = data['Ship Date'].str.split('-', expand=True)
data['Ship Date'] = data['ship_year'] + '/' + data['ship_month'] + '/' + data['ship_day']
data['Ship Date'] = pd.to_datetime(data['Ship Date'])
data.drop(columns=['order_day','order_month','order_year',
                   'ship_day','ship_month','ship_year','Unnamed: 0'], inplace=True)
data['Ship Mode'] = data['Ship Mode'].astype('category')
data['Segment'] = data['Segment'].astype('category')
data['Country'] = data['Country'].astype('category')
data['Market'] = data['Market'].astype('category')
data['Region'] = data['Region'].astype('category')
data['Category'] = data['Category'].astype('category')
data['Sub-Category'] = data['Sub-Category'].astype('category')
data['Order Priority'] = data['Order Priority'].astype('category')


def removespaces(df):
    for cols in df.columns:
        if df[cols].dtypes in ['object','category']:
            df[cols] = df[cols].str.strip()
        return df
    
data = removespaces(data)    
st.title('EDATUM-SAMACHARA DRUSHYA')


def main_page():
    st.sidebar.markdown("# EDATUM 🎈")
    st.subheader('Super Store Dataset')
    st.dataframe(data)
    st.subheader('Numerical Statistics')
    st.dataframe(data.describe())



def page2():
    st.sidebar.markdown("# SAMACHARAM 1 ❄️")
    country_group = data.groupby('Country')
    country_sales = country_group.agg({'Sales':'sum'})
    country_sales.sort_values(by='Sales', ascending=False)
    top_7 = country_sales.nlargest(7, 'Sales')
    top_7.reset_index()


    st.markdown("## Top 7 Countires Vs Total Sales")
    fig = plt.figure(figsize=(5,8))
    explode = [0.08, 0, 0, 0, 0, 0, 0]
    plt.pie(top_7['Sales'],labels=list(top_7.index), explode=explode, shadow=True,
            startangle=90, autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
    st.pyplot(fig)


    st.markdown("## Segment Of Customers VS Profit")
    cust_Seg = data.groupby('Segment')
    df = cust_Seg.aggregate({'Profit':'sum'})
    df.reset_index(inplace=True)
    fig = plt.figure(figsize=(5,8))
    names = df['Segment'].values
    marks = df['Profit'].values
    my_circle = plt.Circle((0, 0), 0.45, color='white')
    plt.pie(marks, labels=names, autopct='%1.1f%%',colors=['red', 'green', 'blue']
        , wedgeprops={'edgecolor': 'black'},startangle=90)
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    st.pyplot(fig)


    st.markdown("## Top 5 Profit-Making Product Types")
    year_category_group = data.groupby(['order year','Sub-Category'])
    year_category_proft_df = year_category_group.agg({'Profit':'sum'})
    year_category_proft_df.reset_index(inplace=True)
    category_yearly_profit = year_category_proft_df.groupby('order year')
    top5_profit_category = pd.DataFrame(columns=year_category_proft_df.columns)

    for g, d in category_yearly_profit:
        high_profit_categories = d.nlargest(5, 'Profit')
        top5_profit_category = pd.concat([top5_profit_category,high_profit_categories])
    
    fig = plt.figure(figsize=(14,11))
    plt.subplot(2, 2, 1)
    x=list(top5_profit_category[top5_profit_category['order year'] == 2012]['Sub-Category'])
    y=top5_profit_category[top5_profit_category['order year'] == 2012]['Profit']
    sns.barplot(x=x,y=y,palette='husl')
    plt.title("Year-2012")

    plt.subplot(2, 2, 2)
    x=list(top5_profit_category[top5_profit_category['order year'] == 2013]['Sub-Category'])
    y=top5_profit_category[top5_profit_category['order year'] == 2013]['Profit']
    sns.barplot(x=x,y=y,palette='Paired')
    plt.title("Year-2013")

    plt.subplot(2, 2, 3)
    x=list(top5_profit_category[top5_profit_category['order year'] == 2014]['Sub-Category'])
    y=top5_profit_category[top5_profit_category['order year'] == 2014]['Profit']
    sns.barplot(x=x,y=y)
    plt.title("Year-2014")

    plt.subplot(2, 2, 4)
    x=list(top5_profit_category[top5_profit_category['order year'] == 2015]['Sub-Category'])
    y=top5_profit_category[top5_profit_category['order year'] == 2015]['Profit']
    sns.barplot(x=x,y=y, palette='hls')
    plt.title("Year-2015")
    st.pyplot(fig)


    st.markdown("## Delivery Speeds Of Top 20 Countries")
    top_20_sales = country_sales.nlargest(20, 'Sales')
    data['Delivery Duration'] = data['Ship Date']-data['Order Date']
    country_group = data.groupby('Country')
    delivery_duration_df = country_group.agg({'Delivery Duration':'mean'})
    delivery_duration_df['Duration In Hours'] = delivery_duration_df['Delivery Duration'] / dt.timedelta(hours=1)
    top20_sales_country_DD =top_20_sales.merge(delivery_duration_df, how='left', left_index=True, right_index=True)
    top20_sales_country_DD.reset_index(inplace=True)
    top20_sales_country_DD.sort_values(by='Duration In Hours')
    labels = []
    for time in list(top20_sales_country_DD['Duration In Hours']):
        if 83 <= time <= 94: labels.append('Fast')
        elif 94 <= time <= 99: labels.append('Average')
        else: labels.append('Slow')
    fig = plt.figure(figsize=(10,5))
    x = list(top20_sales_country_DD['Country'])
    y = list(top20_sales_country_DD['Duration In Hours'])
    sns.scatterplot(x=x,y=y,s=80,hue=labels,palette='Dark2')
    plt. legend(loc='upper left')
    plt.xticks(rotation=90)
    st.pyplot(fig)


def page3():
    st.sidebar.markdown("# SAMACHARAM 2 🎉")
    st.markdown("## Profit Vs Month")
    df_month = data.groupby(['order month','order year'])
    df_pro = df_month.aggregate({'Profit':'sum'})
    df_sal = df_month.aggregate({'Sales':'sum'})
    df_pro.reset_index(inplace=True)
    df_sal.reset_index(inplace=True)
    df =df_pro.merge(df_sal)
    df['month'] = df['order month'].map({1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',
                                        8:'August',9:'September',10:'October',11:'November',12:'December'})
    fig = px.line(df, x="month", y="Profit", color='order year',markers=True)
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("## Countries VS Sales")
    iso_mapping = {'Afghanistan': 'AFG', 'Akrotiri and Dhekelia – See United Kingdom, The': 'Akrotiri and Dhekelia – See United Kingdom, The', 'Åland Islands': 'ALA', 'Albania': 'ALB', 'Algeria': 'DZA', 'American Samoa': 'ASM', 'Andorra': 'AND', 'Angola': 'AGO', 'Anguilla': 'AIA', 'Antarctica\u200a[a]': 'ATA', 'Antigua and Barbuda': 'ATG', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Aruba': 'ABW', 'Ashmore and Cartier Islands – See Australia.': 'Ashmore and Cartier Islands – See Australia.', 'Australia\u200a[b]': 'AUS', 'Austria': 'AUT', 'Azerbaijan': 'AZE', 'Bahamas (the)': 'BHS', 'Bahrain': 'BHR', 'Bangladesh': 'BGD', 'Barbados': 'BRB', 'Belarus': 'BLR', 'Belgium': 'BEL', 'Belize': 'BLZ', 'Benin': 'BEN', 'Bermuda': 'BMU', 'Bhutan': 'BTN', 'Bolivia (Plurinational State of)': 'BOL', 'Bonaire\xa0Sint Eustatius\xa0Saba': 'BES', 'Bosnia and Herzegovina': 'BIH', 'Botswana': 'BWA', 'Bouvet Island': 'BVT', 'Brazil': 'BRA', 'British Indian Ocean Territory (the)': 'IOT', 'British Virgin Islands – See Virgin Islands (British).': 'British Virgin Islands – See Virgin Islands (British).', 'Brunei Darussalam\u200a[e]': 'BRN', 'Bulgaria': 'BGR', 'Burkina Faso': 'BFA', 'Burma – See Myanmar.': 'Burma – See Myanmar.', 'Burundi': 'BDI', 'Cabo Verde\u200a[f]': 'CPV', 'Cambodia': 'KHM', 'Cameroon': 'CMR', 'Canada': 'CAN', 'Cape Verde – See Cabo Verde.': 'Cape Verde – See Cabo Verde.', 'Caribbean Netherlands – See Bonaire, Sint Eustatius and Saba.': 'Caribbean Netherlands – See Bonaire, Sint Eustatius and Saba.', 'Cayman Islands (the)': 'CYM', 'Central African Republic (the)': 'CAF', 'Chad': 'TCD', 'Chile': 'CHL', 'China': 'CHN', 'China, The Republic of – See Taiwan (Province of China).': 'China, The Republic of – See Taiwan (Province of China).', 'Christmas Island': 'CXR', 'Clipperton Island – See France.': 'Clipperton Island – See France.', 'Cocos (Keeling) Islands (the)': 'CCK', 'Colombia': 'COL', 'Comoros (the)': 'COM', 'Congo (the Democratic Republic of the)': 'COD', 'Congo (the)\u200a[g]': 'COG', 'Cook Islands (the)': 'COK', 'Coral Sea Islands – See Australia.': 'Coral Sea Islands – See Australia.', 'Costa Rica': 'CRI', "Côte d'Ivoire\u200a[h]": 'CIV', 'Croatia': 'HRV', 'Cuba': 'CUB', 'Curaçao': 'CUW', 'Cyprus': 'CYP', 'Czechia\u200a[i]': 'CZE', "Democratic People's Republic of Korea – See Korea, The Democratic People's Republic of.": "Democratic People's Republic of Korea – See Korea, The Democratic People's Republic of.", 'Democratic Republic of the Congo – See Congo, The Democratic Republic of the.': 'Democratic Republic of the Congo – See Congo, The Democratic Republic of the.', 'Denmark': 'DNK', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Dominican Republic (the)': 'DOM', 'East Timor – See Timor-Leste.': 'East Timor – See Timor-Leste.', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'El Salvador': 'SLV', 'England – See United Kingdom, The.': 'England – See United Kingdom, The.', 'Equatorial Guinea': 'GNQ', 'Eritrea': 'ERI', 'Estonia': 'EST', 'Eswatini\u200a[j]': 'SWZ', 'Ethiopia': 'ETH', 'Falkland Islands (the) [Malvinas]\u200a[k]': 'FLK', 'Faroe Islands (the)': 'FRO', 'Fiji': 'FJI', 'Finland': 'FIN', 'France\u200a[l]': 'FRA', 'French Guiana': 'GUF', 'French Polynesia': 'PYF', 'French Southern Territories (the)\u200a[m]': 'ATF', 'Gabon': 'GAB', 'Gambia (the)': 'GMB', 'Georgia': 'GEO', 'Germany': 'DEU', 'Ghana': 'GHA', 'Gibraltar': 'GIB', 'Great Britain – See United Kingdom, The.': 'Great Britain – See United Kingdom, The.', 'Greece': 'GRC', 'Greenland': 'GRL', 'Grenada': 'GRD', 'Guadeloupe': 'GLP', 'Guam': 'GUM', 'Guatemala': 'GTM', 'Guernsey': 'GGY', 'Guinea': 'GIN', 'Guinea-Bissau': 'GNB', 'Guyana': 'GUY', 'Haiti': 'HTI', 'Hawaiian Islands – See United States of America, The.': 'Hawaiian Islands – See United States of America, The.', 'Heard Island and McDonald Islands': 'HMD', 'Holy See (the)\u200a[n]': 'VAT', 'Honduras': 'HND', 'Hong Kong': 'HKG', 'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IND', 'Indonesia': 'IDN', 'Iran (Islamic Republic of)': 'IRN', 'Iraq': 'IRQ', 'Ireland': 'IRL', 'Isle of Man': 'IMN', 'Israel': 'ISR', 'Italy': 'ITA', "Ivory Coast – See Côte d'Ivoire.": "Ivory Coast – See Côte d'Ivoire.", 'Jamaica': 'JAM', 'Jan Mayen – See Svalbard and Jan Mayen.': 'Jan Mayen – See Svalbard and Jan Mayen.', 'Japan': 'JPN', 'Jersey': 'JEY', 'Jordan': 'JOR', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kiribati': 'KIR', "Korea (the Democratic People's Republic of)\u200a[o]": 'PRK', 'Korea (the Republic of)\u200a[p]': 'KOR', 'Kuwait': 'KWT', 'Kyrgyzstan': 'KGZ', "Lao People's Democratic Republic (the)\u200a[q]": 'LAO', 'Latvia': 'LVA', 'Lebanon': 'LBN', 'Lesotho': 'LSO', 'Liberia': 'LBR', 'Libya': 'LBY', 'Liechtenstein': 'LIE', 'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Macao\u200a[r]': 'MAC', 'North Macedonia\u200a[s]': 'MKD', 'Madagascar': 'MDG', 'Malawi': 'MWI', 'Malaysia': 'MYS', 'Maldives': 'MDV', 'Mali': 'MLI', 'Malta': 'MLT', 'Marshall Islands (the)': 'MHL', 'Martinique': 'MTQ', 'Mauritania': 'MRT', 'Mauritius': 'MUS', 'Mayotte': 'MYT', 'Mexico': 'MEX', 'Micronesia (Federated States of)': 'FSM', 'Moldova (the Republic of)': 'MDA', 'Monaco': 'MCO', 'Mongolia': 'MNG', 'Montenegro': 'MNE', 'Montserrat': 'MSR', 'Morocco': 'MAR', 'Mozambique': 'MOZ', 'Myanmar\u200a[t]': 'MMR', 'Namibia': 'NAM', 'Nauru': 'NRU', 'Nepal': 'NPL', 'Netherlands (the)': 'NLD', 'New Caledonia': 'NCL', 'New Zealand': 'NZL', 'Nicaragua': 'NIC', 'Niger (the)': 'NER', 'Nigeria': 'NGA', 'Niue': 'NIU', 'Norfolk Island': 'NFK', "North Korea – See Korea, The Democratic People's Republic of.": "North Korea – See Korea, The Democratic People's Republic of.", 'Northern Ireland – See United Kingdom, The.': 'Northern Ireland – See United Kingdom, The.', 'Northern Mariana Islands (the)': 'MNP', 'Norway': 'NOR', 'Oman': 'OMN', 'Pakistan': 'PAK', 'Palau': 'PLW', 'Palestine, State of': 'PSE', 'Panama': 'PAN', 'Papua New Guinea': 'PNG', 'Paraguay': 'PRY', "People's Republic of China – See China.": "People's Republic of China – See China.", 'Peru': 'PER', 'Philippines (the)': 'PHL', 'Pitcairn\u200a[u]': 'PCN', 'Poland': 'POL', 'Portugal': 'PRT', 'Puerto Rico': 'PRI', 'Qatar': 'QAT', 'Republic of China – See Taiwan (Province of China).': 'Republic of China – See Taiwan (Province of China).', 'Republic of Korea – See Korea, The Republic of.': 'Republic of Korea – See Korea, The Republic of.', 'Republic of the Congo – See Congo, The.': 'Republic of the Congo – See Congo, The.', 'Réunion': 'REU', 'Romania': 'ROU', 'Russian Federation (the)\u200a[v]': 'RUS', 'Rwanda': 'RWA', 'Saba – See Bonaire, Sint Eustatius and Saba.': 'Saba – See Bonaire, Sint Eustatius and Saba.', 'Sahrawi Arab Democratic Republic – See Western Sahara.': 'Sahrawi Arab Democratic Republic – See Western Sahara.', 'Saint Barthélemy': 'BLM', 'Saint Helena\xa0Ascension Island\xa0Tristan da Cunha': 'SHN', 'Saint Kitts and Nevis': 'KNA', 'Saint Lucia': 'LCA', 'Saint Martin (French part)': 'MAF', 'Saint Pierre and Miquelon': 'SPM', 'Saint Vincent and the Grenadines': 'VCT', 'Samoa': 'WSM', 'San Marino': 'SMR', 'Sao Tome and Principe': 'STP', 'Saudi Arabia': 'SAU', 'Scotland – See United Kingdom, The.': 'Scotland – See United Kingdom, The.', 'Senegal': 'SEN', 'Serbia': 'SRB', 'Seychelles': 'SYC', 'Sierra Leone': 'SLE', 'Singapore': 'SGP', 'Sint Eustatius – See Bonaire, Sint Eustatius and Saba.': 'Sint Eustatius – See Bonaire, Sint Eustatius and Saba.', 'Sint Maarten (Dutch part)': 'SXM', 'Slovakia': 'SVK', 'Slovenia': 'SVN', 'Solomon Islands': 'SLB', 'Somalia': 'SOM', 'South Africa': 'ZAF', 'South Georgia and the South Sandwich Islands': 'SGS', 'South Korea – See Korea, The Republic of.': 'South Korea – See Korea, The Republic of.', 'South Sudan': 'SSD', 'Spain': 'ESP', 'Sri Lanka': 'LKA', 'Sudan (the)': 'SDN', 'Suriname': 'SUR', 'Svalbard\xa0Jan Mayen': 'SJM', 'Sweden': 'SWE', 'Switzerland': 'CHE', 'Syrian Arab Republic (the)\u200a[x]': 'SYR', 'Taiwan (Province of China)\u200a[y]': 'TWN', 'Tajikistan': 'TJK', 'Tanzania, the United Republic of': 'TZA', 'Thailand': 'THA', 'Timor-Leste\u200a[aa]': 'TLS', 'Togo': 'TGO', 'Tokelau': 'TKL', 'Tonga': 'TON', 'Trinidad and Tobago': 'TTO', 'Tunisia': 'TUN', 'Turkey': 'TUR', 'Turkmenistan': 'TKM', 'Turks and Caicos Islands (the)': 'TCA', 'Tuvalu': 'TUV', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'United Arab Emirates (the)': 'ARE', 'United Kingdom of Great Britain and Northern Ireland (the)': 'GBR', 'United States Minor Outlying Islands (the)\u200a[ac]': 'UMI', 'United States of America (the)': 'USA', 'United States Virgin Islands – See Virgin Islands (U.S.).': 'United States Virgin Islands – See Virgin Islands (U.S.).', 'Uruguay': 'URY', 'Uzbekistan': 'UZB', 'Vanuatu': 'VUT', 'Vatican City – See Holy See, The.': 'Vatican City – See Holy See, The.', 'Venezuela (Bolivarian Republic of)': 'VEN', 'Viet Nam\u200a[ae]': 'VNM', 'Virgin Islands (British)\u200a[af]': 'VGB', 'Virgin Islands (U.S.)\u200a[ag]': 'VIR', 'Wales – See United Kingdom, The.': 'Wales – See United Kingdom, The.', 'Wallis and Futuna': 'WLF', 'Western Sahara\u200a[ah]': 'ESH', 'Yemen': 'YEM', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE', 'United States': 'USA', 'United Kingdom': 'GBR', 'Venezuela': 'VEN', 'Australia': 'AUS', 'Iran': 'IRN', 'France': 'FRA', 'Russia': 'RUS', 'Korea, North': 'PRK', 'Korea, South': 'KOR', 'Myanmar': 'MMR', 'Burma': 'MMR', 'Vietnam': 'VNM', 'Laos': 'LAO', 'Bolivia': 'BOL', 'Niger': 'NER', 'Sudan': 'SDN', 'Congo, Dem. Rep.': 'COD', 'Congo, Repub. of the': 'COG', 'Tanzania': 'TZA', 'Central African Rep.': 'CAF', "Cote d'Ivoire": 'CIV'}
    country_group = data.groupby('Country')
    country_sales = country_group.agg({'Sales':'sum'})
    df = country_sales.reset_index()
    df['ISO Code'] = df['Country'].map(iso_mapping)
    fig = px.choropleth(df, locations="ISO Code",
                        color="Sales", 
                        hover_name="Country",
                        color_continuous_scale='Reds')
    st.plotly_chart(fig,use_container_width=True)


page_names_to_funcs = {
    "EDATUM": main_page,
    "SAMACHARAM 1": page2,
    "SAMACHARAM 2": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()