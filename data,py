import streamlit as st
import yfinance as yf
import datetime

def get_data(symbol, start, end, interval):
    df = yf.download(symbol, start=start, end=end, interval=interval)
    df.index = df.index.tz_localize('UTC').tz_convert('Asia/Kolkata')
    return df

# Get historical data
symbol = "btc-usd"
start_date = "2023-12-19"
end_date = datetime.datetime.now()
interval = "15m"
df = get_data(symbol, start_date, end_date, interval)

# Streamlit app
st.title("Crypto Historical Data")

# Display historical data table
st.write("Historical Data")
st.dataframe(df.tail())

# You can add more components or visualizations as needed
# For example, a simple line chart
st.line_chart(df['Close'])

# Run the app using: streamlit run app.py
