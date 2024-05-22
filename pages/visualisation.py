import streamlit as st
from app import get_db_connection
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

if 'is_authenticated' not in st.session_state:
    st.switch_page('app.py')


def fetch_stock_prices():
    engine = get_db_connection()
    with engine.connect() as connection:
        result = pd.read_sql_query("SELECT [date], [open], high, low, [close], adj_close, volume FROM StockPrice",
                                   connection)
    return result


def fetch_google_trends():
    engine = get_db_connection()
    with engine.connect() as connection:
        result = pd.read_sql_query("SELECT interestCount, timeRange FROM GoogleTrends", connection)
    return result


def fetch_mining_company():
    engine = get_db_connection()
    with engine.connect() as connection:
        result = pd.read_sql_query("SELECT elementPrice, dateTime FROM MiningCompany", connection)
    return result

def fetch_predicted_price():
    engine = get_db_connection()
    with engine.connect() as connection:
        result = pd.read_sql_query("SELECT predictedPrice, date FROM PricePrediction", connection)
    return result


def main():
    st.title("Our Visualisation")

    with st.spinner('Loading data...'):
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_stock_price = executor.submit(fetch_stock_prices)
            future_mining_company = executor.submit(fetch_mining_company)
            future_google_trends = executor.submit(fetch_google_trends)
            future_predicted_price = executor.submit(fetch_predicted_price)

            stock_price = future_stock_price.result()
            mining_company = future_mining_company.result()
            google_trends = future_google_trends.result()
            predicted_price = future_predicted_price.result()

    stock_price['date'] = pd.to_datetime(stock_price['date'])
    st.header("Actual Stock Price Line Chart (USD)")
    st.line_chart(data=stock_price, x='date', y='close', width=1300, height=400)

    google_trends['timeRange'] = pd.to_datetime(google_trends['timeRange'])
    st.header("Google Trends Line Chart (USD)")
    st.line_chart(data=google_trends, x='timeRange', y='interestCount', width=1300, height=400)

    mining_company['dateTime'] = pd.to_datetime(mining_company['dateTime'])
    st.header("Lithium Price Line Chart (USD)")
    st.line_chart(data=mining_company, x='dateTime', y='elementPrice', width=1300, height=400)

    st.header("Actual Stock Price & Predicted Price (USD)")
    stock_price['date'] = pd.to_datetime(stock_price['date'].apply(lambda x: str(x).split()[0])).dt.date
    predicted_price['date'] = pd.to_datetime(predicted_price['date']).dt.date
    combined_data = predicted_price.set_index('date').join(stock_price.set_index('date'), how='inner', lsuffix='_pred', rsuffix='_actual').reset_index()
    print(combined_data)
    st.line_chart(data=combined_data, x='date', y=['close', 'predictedPrice'], width=1300, height=400, color=["#FF0000", "#0000FF"])



if __name__ == '__main__':
    main()
