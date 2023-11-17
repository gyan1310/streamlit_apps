# import streamlit as st
# import pandas as pd
# import numpy as np
# from tqdm import tqdm

# def get_data():
#     df = pd.read_csv("raw_data_15_min.csv")
#     df.set_index("Date", inplace=True)
#     return df

# def calculate_sma(data, sma_s, sma_l):
#     data['SMA_S'] = data['Close'].rolling(sma_s).mean().to_numpy()
#     data['SMA_M'] = data['Close'].rolling(sma_l).mean().to_numpy()
#     data = data.dropna()  # Drop rows with NaN values
#     return data

# def find_up_down(data):
#     up_indices = []
#     down_indices = []

#     for i in range(1, len(data)):
#         if data['SMA_S'][i] > data['SMA_M'][i] and data['SMA_S'][i - 1] <= data['SMA_M'][i - 1]:
#             up_indices.append(i)

#         if data['SMA_S'][i] < data['SMA_M'][i] and data['SMA_S'][i - 1] >= data['SMA_M'][i - 1]:
#             down_indices.append(i)

#     return up_indices, down_indices

# def analyze_segments(data, up_indices, down_indices):
#     merged_indices = sorted(up_indices + down_indices)
    
#     segment_types = []
#     start_indices = []
#     end_indices = []
#     reference_close_prices = []
#     highest_high_prices = []
#     lowest_low_prices = []
#     segment_dates = []

#     for i in range(len(merged_indices) - 1):
#         start_idx = merged_indices[i]
#         end_idx = merged_indices[i + 1]

#         if start_idx in up_indices:
#             segment_type = "up"
#         else:
#             segment_type = "down"

#         reference_close_price = data['Close'][start_idx]
#         highest_high_price = data['High'][start_idx:end_idx].max()
#         lowest_low_price = data['Low'][start_idx:end_idx].min()
#         segment_date = data.index[start_idx]

#         segment_types.append(segment_type)
#         start_indices.append(start_idx)
#         end_indices.append(end_idx)
#         reference_close_prices.append(reference_close_price)
#         highest_high_prices.append(highest_high_price)
#         lowest_low_prices.append(lowest_low_price)
#         segment_dates.append(segment_date)

#     df = pd.DataFrame({
#         'Segment Type': segment_types,
#         'Start Index': start_indices,
#         'End Index': end_indices,
#         'Reference Close Price': reference_close_prices,
#         'Highest High Price': highest_high_prices,
#         'Lowest Low Price': lowest_low_prices,
#         'Segment Date': segment_dates
#     })
#     df['% High Price Difference'] = (df['Highest High Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
#     df['% Low Price Difference'] = (df['Lowest Low Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
#     df['% up-down Difference'] = df['Reference Close Price'].pct_change() * 100
#     df['% up-down Difference'].fillna(0, inplace=True)  # Replace NaN values with 0 for the first row
#     df["bars taken"] = df["End Index"] - df["Start Index"] 
#     df['% up-down Difference'] = df['% up-down Difference'].shift(-1)
#     df['trade_close'] = df['Reference Close Price'].shift(-1)
#     df["Returns"] = df["% up-down Difference"]
#     df.loc[df['Segment Type'] == 'down', 'Returns'] *= -1
#     return df

# def calculate_profit_losses(df):
#     long_profit_trades = 0
#     long_losses_trades = 0
#     short_profit_trades = 0
#     short_losses_trades = 0
#     long_profit = []
#     long_loss = []
#     short_profit = []
#     short_loss = []
#     total_trades = 0
#     profitablity_percent = 0
    
#     for i in range(len(df)):
#         if df["Segment Type"][i] == "up" and df["Returns"][i] > 0:
#             long_profit_trades += 1
#             long_profit.append(df["Returns"][i])
#         elif df["Segment Type"][i] == "up" and df["Returns"][i] < 0:
#             long_losses_trades += 1
#             long_loss.append(df["Returns"][i])

#         if df["Segment Type"][i] == "down" and df["Returns"][i] > 0:
#             short_profit_trades += 1
#             short_profit.append(df["Returns"][i])
#         elif df["Segment Type"][i] == "down" and df["Returns"][i] < 0:
#             short_losses_trades += 1
#             short_loss.append(df["Returns"][i])
#         total_trades = (long_profit_trades
#                         + long_losses_trades
#                         +short_profit_trades
#                         + short_losses_trades)
#         profitablity_percent = ((total_trades -(long_losses_trades+ short_losses_trades))
#                                 / total_trades)*100

#     return pd.DataFrame({
#         'sma_s': [sma_s],
#         'sma_l': [sma_l],
#         'long_profit_trades': [long_profit_trades],
#         'long_losses_trades': [long_losses_trades],
#         'short_profit_trades': [short_profit_trades],
#         'short_losses_trades': [short_losses_trades],
#         'sum_long_profit': [sum(long_profit)],
#         'sum_long_loss': [sum(long_loss)],
#         'sum_short_profit': [sum(short_profit)],
#         'sum_short_loss': [sum(short_loss)],
#         'total_trades': [total_trades],
#         'profitability_percent': [profitablity_percent]
#     })

# # Streamlit App
# st.title("SMA Analysis")

# # Input parameters
# sma_s = st.slider("Select sma_s", min_value=1, max_value=100, value=7)
# sma_l = st.slider("Select sma_l", min_value=1, max_value=250, value=21)

# # Calculate SMA
# df = get_data()
# data = calculate_sma(data=df, sma_s=sma_s, sma_l=sma_l)
# up_indices, down_indices = find_up_down(data)
# segments_df = analyze_segments(data, up_indices, down_indices)
# segments_df.to_csv(f"sma_{sma_s}_{sma_l}.csv", index=False)

# # Display results
# st.write("Segments Data:")
# st.write(segments_df)

# total_returns = segments_df["Returns"].sum()
# pnl = calculate_profit_losses(segments_df)

# # Display P&L
# st.write("Profit and Loss:")
# st.write(pnl)


# import streamlit as st
# import pandas as pd

# def get_data():
#     df = pd.read_csv("raw_data_15_min.csv")
#     df.set_index("Date", inplace=True)
#     return df

# def calculate_sma(data, sma_s, sma_l):
#     data['SMA_S'] = data['Close'].rolling(sma_s).mean().to_numpy()
#     data['SMA_M'] = data['Close'].rolling(sma_l).mean().to_numpy()
#     data = data.dropna()  # Drop rows with NaN values
#     return data

# def find_up_down(data):
#     up_indices = []
#     down_indices = []

#     for i in range(1, len(data)):
#         if data['SMA_S'][i] > data['SMA_M'][i] and data['SMA_S'][i - 1] <= data['SMA_M'][i - 1]:
#             up_indices.append(i)

#         if data['SMA_S'][i] < data['SMA_M'][i] and data['SMA_S'][i - 1] >= data['SMA_M'][i - 1]:
#             down_indices.append(i)

#     return up_indices, down_indices

# def analyze_segments(data, up_indices, down_indices):
#     merged_indices = sorted(up_indices + down_indices)
    
#     segment_types = []
#     start_indices = []
#     end_indices = []
#     reference_close_prices = []
#     highest_high_prices = []
#     lowest_low_prices = []
#     segment_dates = []

#     for i in range(len(merged_indices) - 1):
#         start_idx = merged_indices[i]
#         end_idx = merged_indices[i + 1]

#         if start_idx in up_indices:
#             segment_type = "up"
#         else:
#             segment_type = "down"

#         reference_close_price = data['Close'][start_idx]
#         highest_high_price = data['High'][start_idx:end_idx].max()
#         lowest_low_price = data['Low'][start_idx:end_idx].min()
#         segment_date = data.index[start_idx]

#         segment_types.append(segment_type)
#         start_indices.append(start_idx)
#         end_indices.append(end_idx)
#         reference_close_prices.append(reference_close_price)
#         highest_high_prices.append(highest_high_price)
#         lowest_low_prices.append(lowest_low_price)
#         segment_dates.append(segment_date)

#     df = pd.DataFrame({
#         'Segment Type': segment_types,
#         'Start Index': start_indices,
#         'End Index': end_indices,
#         'Reference Close Price': reference_close_prices,
#         'Highest High Price': highest_high_prices,
#         'Lowest Low Price': lowest_low_prices,
#         'Segment Date': segment_dates
#     })
#     df['% High Price Difference'] = (df['Highest High Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
#     df['% Low Price Difference'] = (df['Lowest Low Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
#     df['% up-down Difference'] = df['Reference Close Price'].pct_change() * 100
#     df['% up-down Difference'].fillna(0, inplace=True)  # Replace NaN values with 0 for the first row
#     df["bars taken"] = df["End Index"] - df["Start Index"] 
#     df['% up-down Difference'] = df['% up-down Difference'].shift(-1)
#     df['trade_close'] = df['Reference Close Price'].shift(-1)
#     df["Returns"] = df["% up-down Difference"]
#     df.loc[df['Segment Type'] == 'down', 'Returns'] *= -1
#     return df

# def calculate_profit_losses(df):
#     long_profit_trades = 0
#     long_losses_trades = 0
#     short_profit_trades = 0
#     short_losses_trades = 0
#     long_profit = []
#     long_loss = []
#     short_profit = []
#     short_loss = []
#     total_trades = 0
#     profitablity_percent = 0
    
#     for i in range(len(df)):
#         if df["Segment Type"][i] == "up" and df["Returns"][i] > 0:
#             long_profit_trades += 1
#             long_profit.append(df["Returns"][i])
#         elif df["Segment Type"][i] == "up" and df["Returns"][i] < 0:
#             long_losses_trades += 1
#             long_loss.append(df["Returns"][i])

#         if df["Segment Type"][i] == "down" and df["Returns"][i] > 0:
#             short_profit_trades += 1
#             short_profit.append(df["Returns"][i])
#         elif df["Segment Type"][i] == "down" and df["Returns"][i] < 0:
#             short_losses_trades += 1
#             short_loss.append(df["Returns"][i])
#         total_trades = (long_profit_trades
#                         + long_losses_trades
#                         +short_profit_trades
#                         + short_losses_trades)
#         profitablity_percent = ((total_trades -(long_losses_trades+ short_losses_trades))
#                                 / total_trades)*100

#     return pd.DataFrame({
#         'sma_s': [sma_s],
#         'sma_l': [sma_l],
#         'long_profit_trades': [long_profit_trades],
#         'long_losses_trades': [long_losses_trades],
#         'short_profit_trades': [short_profit_trades],
#         'short_losses_trades': [short_losses_trades],
#         'sum_long_profit': [sum(long_profit)],
#         'sum_long_loss': [sum(long_loss)],
#         'sum_short_profit': [sum(short_profit)],
#         'sum_short_loss': [sum(short_loss)],
#         'total_trades': [total_trades],
#         'profitability_percent': [profitablity_percent]
#     })

# # Streamlit App
# st.title("SMA Analysis")

# # Input parameters
# sma_s = st.slider("Select sma_s", min_value=1, max_value=100, value=7)
# sma_l = st.slider("Select sma_l", min_value=1, max_value=250, value=21)

# # Button to trigger analysis
# if st.button("Run Analysis"):
#     # Calculate SMA
#     df = get_data()
#     data = calculate_sma(data=df, sma_s=sma_s, sma_l=sma_l)
#     up_indices, down_indices = find_up_down(data)
#     segments_df = analyze_segments(data, up_indices, down_indices)
#     segments_df.to_csv(f"sma_{sma_s}_{sma_l}.csv", index=False)

#     # Display results
#     st.write("Segments Data:")
#     st.write(segments_df)

#     total_returns = segments_df["Returns"].sum()
#     pnl = calculate_profit_losses(segments_df)

#     # Display P&L
#     st.write("Profit and Loss:")
#     st.write(pnl)

# import streamlit as st
# import pandas as pd

# def get_data():
#     df = pd.read_csv("raw_data_15_min.csv")
#     df.set_index("Date", inplace=True)
#     return df

# def calculate_sma(data, sma_s, sma_l):
#     data['SMA_S'] = data['Close'].rolling(sma_s).mean().to_numpy()
#     data['SMA_M'] = data['Close'].rolling(sma_l).mean().to_numpy()
#     data = data.dropna()  # Drop rows with NaN values
#     return data

# def find_up_down(data):
#     up_indices = []
#     down_indices = []

#     for i in range(1, len(data)):
#         if data['SMA_S'][i] > data['SMA_M'][i] and data['SMA_S'][i - 1] <= data['SMA_M'][i - 1]:
#             up_indices.append(i)

#         if data['SMA_S'][i] < data['SMA_M'][i] and data['SMA_S'][i - 1] >= data['SMA_M'][i - 1]:
#             down_indices.append(i)

#     return up_indices, down_indices

# def analyze_segments(data, up_indices, down_indices):
#     merged_indices = sorted(up_indices + down_indices)
    
#     segment_types = []
#     start_indices = []
#     end_indices = []
#     reference_close_prices = []
#     highest_high_prices = []
#     lowest_low_prices = []
#     segment_dates = []

#     for i in range(len(merged_indices) - 1):
#         start_idx = merged_indices[i]
#         end_idx = merged_indices[i + 1]

#         if start_idx in up_indices:
#             segment_type = "up"
#         else:
#             segment_type = "down"

#         reference_close_price = data['Close'][start_idx]
#         highest_high_price = data['High'][start_idx:end_idx].max()
#         lowest_low_price = data['Low'][start_idx:end_idx].min()
#         segment_date = data.index[start_idx]

#         segment_types.append(segment_type)
#         start_indices.append(start_idx)
#         end_indices.append(end_idx)
#         reference_close_prices.append(reference_close_price)
#         highest_high_prices.append(highest_high_price)
#         lowest_low_prices.append(lowest_low_price)
#         segment_dates.append(segment_date)

#     df = pd.DataFrame({
#         'Segment Type': segment_types,
#         'Start Index': start_indices,
#         'End Index': end_indices,
#         'Reference Close Price': reference_close_prices,
#         'Highest High Price': highest_high_prices,
#         'Lowest Low Price': lowest_low_prices,
#         'Segment Date': segment_dates
#     })
#     df['% High Price Difference'] = (df['Highest High Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
#     df['% Low Price Difference'] = (df['Lowest Low Price'] - df['Reference Close Price']) / df['Reference Close Price'] * 100
#     df['% up-down Difference'] = df['Reference Close Price'].pct_change() * 100
#     df['% up-down Difference'].fillna(0, inplace=True)  # Replace NaN values with 0 for the first row
#     df["bars taken"] = df["End Index"] - df["Start Index"] 
#     df['% up-down Difference'] = df['% up-down Difference'].shift(-1)
#     df['trade_close'] = df['Reference Close Price'].shift(-1)
#     df["Returns"] = df["% up-down Difference"]
#     df.loc[df['Segment Type'] == 'down', 'Returns'] *= -1
#     return df

# def calculate_profit_losses(df):
#     long_profit_trades = 0
#     long_losses_trades = 0
#     short_profit_trades = 0
#     short_losses_trades = 0
#     long_profit = []
#     long_loss = []
#     short_profit = []
#     short_loss = []
#     total_trades = 0
#     profitablity_percent = 0
    
#     for i in range(len(df)):
#         if df["Segment Type"][i] == "up" and df["Returns"][i] > 0:
#             long_profit_trades += 1
#             long_profit.append(df["Returns"][i])
#         elif df["Segment Type"][i] == "up" and df["Returns"][i] < 0:
#             long_losses_trades += 1
#             long_loss.append(df["Returns"][i])

#         if df["Segment Type"][i] == "down" and df["Returns"][i] > 0:
#             short_profit_trades += 1
#             short_profit.append(df["Returns"][i])
#         elif df["Segment Type"][i] == "down" and df["Returns"][i] < 0:
#             short_losses_trades += 1
#             short_loss.append(df["Returns"][i])
#         total_trades = (long_profit_trades
#                         + long_losses_trades
#                         +short_profit_trades
#                         + short_losses_trades)
#         profitablity_percent = ((total_trades -(long_losses_trades+ short_losses_trades))
#                                 / total_trades)*100

#     return pd.DataFrame({
#         'sma_s': [sma_s],
#         'sma_l': [sma_l],
#         'long_profit_trades': [long_profit_trades],
#         'long_losses_trades': [long_losses_trades],
#         'short_profit_trades': [short_profit_trades],
#         'short_losses_trades': [short_losses_trades],
#         'sum_long_profit': [sum(long_profit)],
#         'sum_long_loss': [sum(long_loss)],
#         'sum_short_profit': [sum(short_profit)],
#         'sum_short_loss': [sum(short_loss)],
#         'total_trades': [total_trades],
#         'profitability_percent': [profitablity_percent]
#     })

# def perform_trades(data):
#     long = 0 
#     l_long = 0
#     short = 0
#     s_short = 0
#     tp_long = 0.1
#     tp_short = -0.1
#     trade_value = 100
#     portfolio_value = 100
#     loss = 0
#     count = 0
#     for i in range(len(data)-1):
#         if data["Segment Type"].iloc[i] == "up" and data["Returns"].iloc[i] > 0:
#             long += 1
#             profit = trade_value * abs(data["Returns"].iloc[i] / 100) 
#             portfolio_value += profit
#         elif data["Segment Type"].iloc[i] == "down" and data["Returns"].iloc[i] > 0:
#             short += 1
#             profit = trade_value * abs(data["Returns"].iloc[i] / 100) 
#             portfolio_value += profit
#         elif data["Segment Type"].iloc[i] == "up" and data["Returns"].iloc[i] < 0:
#             l_long += 1
#             loss = trade_value * abs(data["Returns"].iloc[i] / 100) 
#             portfolio_value -= loss
#         elif data["Segment Type"].iloc[i] == "down" and data["Returns"].iloc[i] < 0:
#             s_short += 1
#             loss = trade_value * abs(data["Returns"].iloc[i] / 100) 
#             portfolio_value -= loss

#     st.write("Long Trades:", long)
#     st.write("Unsuccessful Long Trades:", l_long)
#     st.write("Short Trades:", short)
#     st.write("Unsuccessful Short Trades:", s_short)
#     st.write("Final Portfolio Value:", portfolio_value)

# # Streamlit App
# st.title("SMA Analysis")

# # Input parameters
# sma_s = st.slider("Select sma_s", min_value=1, max_value=100, value=7)
# sma_l = st.slider("Select sma_l", min_value=1, max_value=250, value=21)

# # Button to trigger analysis
# if st.button("Run Analysis"):
#     # Calculate SMA
#     df = get_data()
#     data = calculate_sma(data=df, sma_s=sma_s, sma_l=sma_l)
#     up_indices, down_indices = find_up_down(data)
#     segments_df = analyze_segments(data, up_indices, down_indices)
#     segments_df.to_csv(f"sma_{sma_s}_{sma_l}.csv", index=False)

#     # Display results
#     st.write("Segments Data:")
#     st.write(segments_df)

#     total_returns = segments_df["Returns"].sum()
#     pnl = calculate_profit_losses(segments_df)

#     # Display P&L
#     st.write("Profit and Loss:")
#     st.write(pnl)

#     # Perform trades
#     perform_trades(segments_df)

