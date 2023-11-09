import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    segments_df = pd.read_csv("raw_data_15_MIN.csv")
    segments_df.set_index("Date", inplace=True)
    segments_df = pd.DataFrame(segments_df)
    return segments_df

# Function to calculate Simple Moving Averages (SMA)
def calculate_sma(data, sma_s, sma_l):
    data["SMA_S"] = data.Close.rolling(window=sma_s).mean()
    data["SMA_M"] = data.Close.rolling(window=sma_l).mean()
    data['Row'] = range(1, len(data) + 1)
    data = data.dropna()
    return data

# Function to find cross_UP and cross_DOWN signals
def find_cross_UP_cross_DOWN(data):
    cross_UP_indices = []
    cross_DOWN_indices = []

    for i in range(1, len(data)):
        if data['SMA_S'][i] > data['SMA_M'][i] and data['SMA_S'][i - 1] <= data['SMA_M'][i - 1]:
            cross_UP_indices.append(i)

        if data['SMA_S'][i] < data['SMA_M'][i] and data['SMA_S'][i - 1] >= data['SMA_M'][i - 1]:
            cross_DOWN_indices.append(i)

    return cross_UP_indices, cross_DOWN_indices

def analyze_segments(data, cross_UP_indices, cross_DOWN_indices):
    merged_indices = sorted(cross_UP_indices + cross_DOWN_indices)
    
    segment_types = []
    start_indices = []
    end_indices = []
    reference_close_prices = []
    highest_high_prices = []
    lowest_low_prices = []
    segment_dates = []

    for i in range(len(merged_indices) - 1):
        start_idx = merged_indices[i]
        end_idx = merged_indices[i + 1]

        if start_idx in cross_UP_indices:
            segment_type = "cross_UP"
        else:
            segment_type = "cross_DOWN"

        reference_close_price = data['Close'][start_idx - 1]
        highest_high_price = data['High'][start_idx:end_idx].max()
        lowest_low_price = data['Low'][start_idx:end_idx].min()
        segment_date = data.index[start_idx - 1]

        segment_types.append(segment_type)
        start_indices.append(start_idx)
        end_indices.append(end_idx)
        reference_close_prices.append(reference_close_price)
        highest_high_prices.append(highest_high_price)
        lowest_low_prices.append(lowest_low_price)
        segment_dates.append(segment_date)

    segments_df = pd.DataFrame({
        'Segment Type': segment_types,
        'Start Index': start_indices,
        'End Index': end_indices,
        'Reference Close Price': reference_close_prices,
        'Highest High Price': highest_high_prices,
        'Lowest Low Price': lowest_low_prices,
        'Segment Date': segment_dates
    })
    segments_df['% High Price Difference'] = (segments_df['Highest High Price'] - segments_df['Reference Close Price']) / segments_df['Reference Close Price'] * 100
    segments_df['% Low Price Difference'] = (segments_df['Lowest Low Price'] - segments_df['Reference Close Price']) / segments_df['Reference Close Price'] * 100
    segments_df['% cross_UP-cross_DOWN Difference'] = segments_df['Reference Close Price'].pct_change() * 100
    segments_df['% cross_UP-cross_DOWN Difference'].fillna(0, inplace=True)  # Replace NaN values with 0 for the first row
    segments_df["bars taken"] = segments_df["End Index"] - segments_df["Start Index"] 
    segments_df['% cross_UP-cross_DOWN Difference'] = segments_df['% cross_UP-cross_DOWN Difference'].shift(-1)
    segments_df['trade_close'] = segments_df['Reference Close Price'].shift(-1)
    segments_df["Returns"] = segments_df["% cross_UP-cross_DOWN Difference"]
    segments_df.loc[segments_df['Segment Type'] == 'cross_DOWN', 'Returns'] *= -1
    return segments_df

def calculate_profit_losses(segments_df):
    long_profit_trades = 0
    long_losses_trades = 0
    short_profit_trades = 0
    short_losses_trades = 0
    long_profit = []
    long_loss = []
    short_profit = []
    short_loss = []
    total_trades = 0
    profitablity_percent = 0
    
    for i in range(len(segments_df)):
        if segments_df["Segment Type"][i] == "cross_UP" and segments_df["Returns"][i] > 0:
            long_profit_trades += 1
            long_profit.append(segments_df["Returns"][i])
        elif segments_df["Segment Type"][i] == "cross_UP" and segments_df["Returns"][i] < 0:
            long_losses_trades += 1
            long_loss.append(segments_df["Returns"][i])

        if segments_df["Segment Type"][i] == "cross_DOWN" and segments_df["Returns"][i] > 0:
            short_profit_trades += 1
            short_profit.append(segments_df["Returns"][i])
        elif segments_df["Segment Type"][i] == "cross_DOWN" and segments_df["Returns"][i] < 0:
            short_losses_trades += 1
            short_loss.append(segments_df["Returns"][i])
        total_trades = (long_profit_trades
                        + long_losses_trades
                        +short_profit_trades
                        + short_losses_trades)
        profitablity_percent = ((total_trades -(long_losses_trades+ short_losses_trades))
                                / total_trades)*100

    return (
        long_profit_trades,
        long_losses_trades,
        short_profit_trades,
        short_losses_trades,
        sum(long_profit),
        sum(long_loss),
        sum(short_profit),
        sum(short_loss),
        total_trades,
        profitablity_percent
    )

# Streamlit app
def main():
    st.title('SMA Analysis and Visualization')

    # User input for SMA values
    sma_s = st.sidebar.slider('Select Short-term SMA window', 1, 50, 1)
    sma_l = st.sidebar.slider('Select Long-term SMA window', 1, 50, 10)

    # Display user-selected SMA values
    st.sidebar.text( sma_s)
    st.sidebar.text( sma_l)

    # Load data
    segments_df = get_data()

    # Calculate SMA
    data = calculate_sma(data=segments_df, sma_s=sma_s, sma_l=sma_l)

    # Find cross_UP and cross_DOWN signals
    cross_UP_indices, cross_DOWN_indices = find_cross_UP_cross_DOWN(data)

    # Analyze segments
    segments_df = analyze_segments(data, cross_UP_indices, cross_DOWN_indices)

    # Display DataFrame with selected columns
    st.dataframe(segments_df[['Segment Type', 'Reference Close Price', 'trade_close', 'Returns', 'Highest High Price', 'Lowest Low Price', '% High Price Difference', '% Low Price Difference', '% cross_UP-cross_DOWN Difference', 'bars taken', 'Segment Date', 'Start Index', 'End Index']])

    # Display Profit and Loss Summary
    st.subheader('Profit and Loss Summary')
    profit_loss_data = calculate_profit_losses(segments_df)
    profitability_data = pd.DataFrame({
        "Metric": ["Total trades", "Number of profitable long trades", "Number of losing long trades",
                   "Number of profitable short trades", "Number of losing short trades",
                   "Total profit from long trades", "Total loss from long trades",
                   "Total profit from short trades", "Total loss from short trades",
                   "Percentage Profitability"],
        "Value": [profit_loss_data[8], profit_loss_data[0], profit_loss_data[1],
                  profit_loss_data[2], profit_loss_data[3], profit_loss_data[4],
                  profit_loss_data[5], profit_loss_data[6], profit_loss_data[7],
                  profit_loss_data[9]]
    })
    st.dataframe(profitability_data)

    # Filter data for a particular date range
    start_date = st.sidebar.date_input('Select start date', min(data.index))
    end_date = st.sidebar.date_input('Select end date', max(data.index))
    filtered_data = segments_df[(segments_df['Segment Date'] >= start_date) & (segments_df['Segment Date'] <= end_date)]
    st.subheader(f'Data for the selected date range: {start_date} to {end_date}')
    st.dataframe(filtered_data[['Segment Type', 'Reference Close Price', 'trade_close', 'Returns', 'Highest High Price', 'Lowest Low Price', '% High Price Difference', '% Low Price Difference', '% cross_UP-cross_DOWN Difference', 'bars taken', 'Segment Date', 'Start Index', 'End Index']])

if __name__ == '__main__':
    main()
