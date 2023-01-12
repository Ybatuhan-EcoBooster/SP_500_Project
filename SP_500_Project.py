#streamlit run your_script.py (Streamlit working command)

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import datapackage
import plotly.graph_objects as go

###### S&P 500 Tickers #######
data_url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'

package = datapackage.Package(data_url)
# to load only tabular data

resources = package.resources

for resource in resources:
    if resource.tabular:
        SP_500 = pd.read_csv(resource.descriptor['path'])


SP_500_df = SP_500
SP_500_tickers = SP_500['Symbol'].tolist()
SP_500_tickers = list(set(SP_500_tickers))


############## Create Frame ######################
header = st.container()
text= st.container()

My_Stocks = st.container()
date = st.container()
My_Profile = st.container()

Ticker_list = st.container()

dataset = st.container()
SP500 = st.container()
candle_stick = st.container()

features = st.container()
names_data = st.container()


with header:
    st.title('Welcome to ')
    st.title('My S&P 500 data project!👨‍💻')
    st.error('In this project I prepared to search S&P 500 Portfolio Data set❗')
    with text:
        st.text('''----The S&P 500 Index, or Standard & Poor's 500 Index,\n is a market-capitalization-weighted index \n of 500 leading publicly traded companies in the U.S.---''')
        st.text('''for more information you can visit this website :''')
        st.info('https://www.investopedia.com/terms/s/sp500.asp')

with My_Stocks:
    with st.sidebar:
        st.title('My S&P 500 Portfolio 📥')
        with Ticker_list:
                ticker_list = st.sidebar.text_input('Write your Ticker (ex. AAPL,HPQ,AMZN)')
                if ticker_list is not None:
                    textsplit = ticker_list.replace(' ',',').replace('.',',').split(',')

        with date:
            start_date = st.sidebar.date_input('Start Date', datetime.date(2022, 1, 1))
            st.sidebar.write(start_date)
            end_date = st.sidebar.date_input('End Date',datetime.date(2023,1,1))
            st.sidebar.write(end_date)
        with My_Profile:
            st.sidebar.text('🥷My Linkedin Account ')
            st.sidebar.info('https://www.linkedin.com/in/batuhannyildirim/')
            st.sidebar.text('🥷Github Profile')
            st.sidebar.info('https://github.com/Ybatuhan-EcoBooster')

with dataset:
        st.success(f'S&P 500 List Tickers:{textsplit}', icon=None)
        with SP500:
            list = sorted(textsplit)
            result = set(SP_500_tickers).intersection(set(list))
            SP500= st.multiselect('Select your S&P 500 Ticker',result)
            tab1, tab2 = st.tabs(["📈 Chart", "📅 Data"])
            if SP500:
                tab2.header('My S&P 500 Portfolio dataset')
                tab2.text('This dataset come from on Yahoo Finance')
                SP_500_Stocks = yf.download(SP500, start_date, end_date)
                tab2.write(SP_500_Stocks)

                tab1.subheader('My S&P 500 Portfolio Companies Closing Price with Line Chart')
                closing_prices_df = SP_500_Stocks['Adj Close']
                tab1.line_chart(closing_prices_df)
            else:
                tab2.header('My S&P 500 Portfolio dataset')
                tab2.text('This dataset come from on Yahoo Finance')
                SP_500_Stocks = yf.download(list, start_date, end_date)
                tab2.write(SP_500_Stocks)

                tab1.subheader('My S&P 500 Portfolio Companies Closing Price with Line Chart')
                closing_prices_df = SP_500_Stocks['Adj Close']
                tab1.line_chart(closing_prices_df)


SP_500_sector = SP_500['Sector'].tolist()
SP_500_sector = sorted(set(SP_500_sector))
SP_500_sector_count =SP_500['Sector'].value_counts().sort_index().tolist()

My_SP500 = []
for i in SP_500['Symbol']:
    for k in result:
        if i == k:
            My_SP500.append(k)

My_SP500_merged_table = SP_500[SP_500['Symbol'].isin(My_SP500)]
My_SP500_Sector = My_SP500_merged_table['Sector'].tolist()
My_SP500_Sector = sorted(set(My_SP500_Sector))
My_SP500_Sector_count = My_SP500_merged_table['Sector'].value_counts().sort_index().tolist()

with candle_stick:
    st.header('Candle Stick Graph')
    list_1 = sorted(textsplit)
    result_1 = set(SP_500_tickers).intersection(set(list_1))
    New_SP500 = st.selectbox('Select your S&P 500 Ticker',result_1)
    if New_SP500:
        New_SP500_Stocks = yf.download(result_1, start_date, end_date)
        CandleStick = go.Figure(data=[go.Candlestick(x=New_SP500_Stocks.index,
                                                     open=New_SP500_Stocks[('Open', f'{New_SP500}')],
                                                     high=New_SP500_Stocks[('High', f'{New_SP500}')],
                                                     low=New_SP500_Stocks[('Low', f'{New_SP500}')],
                                                     close=New_SP500_Stocks[('Close', f'{New_SP500}')])])
        st.plotly_chart(CandleStick)
    else:
        st.option = False

with features:
    st.header('S&P 500 Companies Sectoral Distribution Data Set')
    tab3,tab4 = st.tabs(["📈 S&P 500 Distribution", "📈 MY S&P 500 List Distribution "])
    Pie_chart = go.Figure(data=[go.Pie(labels=SP_500_sector, values=SP_500_sector_count, textinfo='label+percent',
                                insidetextorientation='radial', name='Sector Names'
                                )])
    Pie_chart.update_layout(title_text="S&P 500 Companies Sectoral Distribution (%)", legend_title_text='Names of Sector: ',
                      template="plotly_dark")
    tab3.plotly_chart(Pie_chart,theme=None, use_container_width=True)
    fig_1 = go.Figure(data=[go.Pie(labels=My_SP500_Sector, values=My_SP500_Sector_count, textinfo='label+percent',
                                   insidetextorientation='radial', name='Sector Names'
                                   )])
    fig_1.update_layout(title_text="S&P 500 Companies Sectoral Distribution (%)", legend_title_text='Names of Sector: ',
                        template="plotly_dark")
    tab4.plotly_chart(fig_1, theme=None, use_container_width=True)


with names_data:
    st.header('S&P 500 Companies Names 🏢')
    tab5,tab6 = st.tabs(['📄S&P 500 Companies','📄 My S&P 500'])
    SP500_table = SP_500
    tab5.dataframe(SP500_table)

    My_SP500_table =My_SP500_merged_table
    tab6.dataframe(My_SP500_table)



