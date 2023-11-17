
import streamlit as st
import pandas as pd
import numpy as np

def get_data():
    df = pd.read_csv("linkedin.csv")
    df.set_index("Date", inplace=True)
    return df

def calculate_sma(data, sma_s, sma_l, ma_type):
    if ma_type == "EMA_SMA":
        data['SMA_S'] = data['Close'].ewm(span=sma_s, adjust=False).mean()
        data['SMA_M'] = data['Close'].rolling(window=sma_l).mean()
        data = data.dropna()
        
    elif ma_type == "SMA_EMA":
        data['SMA_S'] = data['Close'].rolling(window=sma_s).mean()
        data['SMA_M'] = data['Close'].ewm(span=sma_l, adjust=False).mean()
        data = data.dropna()
        
    elif ma_type == "SMA_SMA":
        data['SMA_S'] = data['Close'].rolling(window=sma_s).mean()
        data['SMA_M'] = data['Close'].rolling(window=sma_l).mean()
        data = data.dropna()
        
    elif ma_type == "EMA_EMA":
        data['SMA_S'] = data['Close'].ewm(span=sma_s, adjust=False).mean()
        data['SMA_M'] = data['Close'].ewm(span=sma_l, adjust=False).mean()
        data = data.dropna()
        
    return data

def find_up_down(data):
    up_indices = []
    down_indices = []

    for i in range(1, len(data)):
        if data['SMA_S'][i] > data['SMA_M'][i] and data['SMA_S'][i - 1] <= data['SMA_M'][i - 1]:
            up_indices.append(i)

        if data['SMA_S'][i] < data['SMA_M'][i] and data['SMA_S'][i - 1] >= data['SMA_M'][i - 1]:
            down_indices.append(i)

    return up_indices, down_indices

def analyze_segments(data, up_indices, down_indices):
    merged_indices = sorted(up_indices + down_indices)
    
    segment_types = []
    start_indices = []
    end_indices = []
    reference_close_prices = []
    highest_high_prices = []
    lowest_low_prices = []
    segment_dates = []

    for i in range(len(merged_indices)-1):
        start_idx = merged_indices[i]
        end_idx = merged_indices[i + 1]

        if start_idx in up_indices:
            segment_type = "up"
        else:
            segment_type = "down"

        reference_close_price = data['Close'][start_idx]
        highest_high_price = data['High'][start_idx:end_idx].max()
        lowest_low_price = data['Low'][start_idx:end_idx].min()
        segment_date = data.index[start_idx]

        segment_types.append(segment_type)
        start_indices.append(start_idx)
        end_indices.append(end_idx)
        reference_close_prices.append(reference_close_price)
        highest_high_prices.append(highest_high_price)
        lowest_low_prices.append(lowest_low_price)
        segment_dates.append(segment_date)

    df = pd.DataFrame({
        'Segment Type': segment_types,
        'Start Index': start_indices,
        'End Index': end_indices,
        'Reference Close Price': reference_close_prices,
        'Highest High Price': highest_high_prices,
        'Lowest Low Price': lowest_low_prices,
        'Segment Date': segment_dates
    })
    df['% High Price Difference'] = (df['Highest High Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
    df['% Low Price Difference'] = (df['Lowest Low Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
    df['% up-down Difference'] = df['Reference Close Price'].pct_change() * 100
    df['% up-down Difference'].fillna(0, inplace=True)  # Replace NaN values with 0 for the first row
    df["bars taken"] = df["End Index"] - df["Start Index"] 
    df['% up-down Difference'] = df['% up-down Difference'].shift(-1)
    df['trade_close'] = df['Reference Close Price'].shift(-1)
    df["Returns"] = df["% up-down Difference"]
    df.loc[df['Segment Type'] == 'down', 'Returns'] *= -1
    return df

def calculate_profit_losses(df, trade_type, sma_s, sma_l):
    long_profit_trades = 0
    long_losses_trades = 0
    short_profit_trades = 0
    short_losses_trades = 0
    long_profit = []
    long_loss = []
    short_profit = []
    short_loss = []
    total_trades = 0
    trade_value = 100
    portfolio_value = 0

    
    for i in range(len(df)):
        if trade_type == "Long":
            
            if df["Segment Type"][i] == "up" and df["Returns"][i] > 0:
                long_profit_trades += 1
                long_profit.append(df["Returns"][i])
                profit = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value += profit
            
            elif df["Segment Type"][i] == "up" and df["Returns"][i] < 0:
                long_losses_trades += 1
                long_loss.append(df["Returns"][i])
                loss = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value -= loss
                
            total_trades = (long_profit_trades
                            + long_losses_trades)
                
        elif trade_type == "Short":
            
            if df["Segment Type"][i] == "down" and df["Returns"][i] > 0:
                short_profit_trades += 1
                short_profit.append(df["Returns"][i])
                profit = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value += profit

            elif df["Segment Type"][i] == "down" and df["Returns"][i] < 0:
                short_losses_trades += 1
                short_loss.append(df["Returns"][i])
                loss = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value -= loss
                
            total_trades = (short_profit_trades
                            + short_losses_trades)
                
        elif trade_type == "Both":
            
            if df["Segment Type"][i] == "up" and df["Returns"][i] > 0:
                long_profit_trades += 1
                long_profit.append(df["Returns"][i])
                profit = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value += profit

            elif df["Segment Type"][i] == "up" and df["Returns"][i] < 0:
                long_losses_trades += 1
                long_loss.append(df["Returns"][i])
                loss = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value -= loss

            if df["Segment Type"][i] == "down" and df["Returns"][i] > 0:
                short_profit_trades += 1
                short_profit.append(df["Returns"][i])
                profit = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value += profit

            elif df["Segment Type"][i] == "down" and df["Returns"][i] < 0:
                short_losses_trades += 1
                short_loss.append(df["Returns"][i])
                loss = trade_value * abs(df["Returns"][i] / 100) 
                portfolio_value -= loss
            
            total_trades = (long_profit_trades
                            + long_losses_trades
                            +short_profit_trades
                            + short_losses_trades)


    return pd.DataFrame({
        'sma_s': [sma_s],
        'sma_l': [sma_l],
        'trade_type': [trade_type],
        'long_profit_trades': (long_profit_trades),
        'long_losses_trades': (long_losses_trades),
        'short_profit_trades': (short_profit_trades),
        'short_losses_trades': (short_losses_trades),
        'sum_long_profit': sum(long_profit),
        'sum_long_loss': sum(long_loss),
        'sum_short_profit': sum(short_profit),
        'sum_short_loss': sum(short_loss),
        'total_trades': total_trades,
        "portfolio_value" : portfolio_value

    })

# Streamlit app
def main():
    st.title("Moving Average Trading Analysis")

    # Sidebar options
    sma_s = st.sidebar.slider("Select SMA Short Window", 1, 100, 21)
    sma_l = st.sidebar.slider("Select SMA Long Window", 1, 100, 50)
    ma_type = st.sidebar.selectbox("Select Moving Average Combination", ["EMA_SMA", "SMA_EMA", "SMA_SMA", "EMA_EMA"])
    trade_type = st.sidebar.radio("Select Trade Type", ["Long", "Short", "Both"])

    # Load data and perform analysis
    df = get_data()
    data = calculate_sma(df, sma_s, sma_l, ma_type)
    up_indices, down_indices = find_up_down(data)
    segments_df = analyze_segments(data, up_indices, down_indices)
    segments_df.to_csv(f"sma_{sma_s}_{sma_l}_{ma_type}.csv", index=False)

    # Display results
    st.dataframe(segments_df)
    total_returns = segments_df["Returns"].sum()
    st.info(f"Total Returns: {total_returns}")

    # Calculate profit and losses
    pnl = calculate_profit_losses(segments_df, trade_type, sma_s, sma_l)
    st.dataframe(pnl)

if __name__ == "__main__":
    main()
