

---

## Moving Average Trading Analysis User Guide

### Introduction:

Welcome to the Moving Average Trading Analysis app! This tool helps you analyze historical stock data and implement a trading strategy based on Moving Averages.

### Getting Started:

1. **User Input:**
   - On the left sidebar, you'll find the "User Input" section. Here, you can customize your analysis by providing the following information:
     - **Symbol (e.g., BTC-USD):** Enter the stock symbol you want to analyze (default: "BTC-USD").
     - **Start Date:** Select the start date for historical data.
     - **End Date:** Select the end date for historical data.
     - **SMA Short Window:** Choose the window size for the Short Simple Moving Average (SMA).
     - **SMA Long Window:** Choose the window size for the Long Simple Moving Average (SMA).
     - **Moving Average Combination:** Select the type of Moving Average combination to use (options: EMA_SMA, SMA_EMA, SMA_SMA, EMA_EMA).
     - **Trade Type:** Choose the trading strategy (options: Long, Short, Both).

2. **Testing the Analysis:**
   - After entering your preferences, click the "Test" button to initiate the analysis.

### Results:

1. **Historical Data:**
   - The initial section displays the historical data for the selected stock.

2. **Trading Signals:**
   - A chart is displayed showing the closing price of the stock along with the Short and Long Simple Moving Averages.

3. **Equity Curve:**
   - An equity curve chart is shown, representing the portfolio value over time based on the trading strategy.

4. **Returns Chart:**
   - A chart illustrating the returns over time based on the trading strategy.

5. **Trade Summary:**
   - A bar chart providing a summary of the number of profitable and losing trades for both long and short positions, along with the total number of trades.

6. **Profit and Loss Summary:**
   - A table summarizing the key statistics of the analysis, including the number of profitable and losing trades, total returns, and more.

### Interpreting the Results:

- **Total Returns:**
  - The total returns percentage is displayed at the top, indicating the overall performance of the selected trading strategy.

- **Trade Summary:**
  - The bar chart gives a visual representation of the number of profitable and losing trades for both long and short positions.

- **Profit and Loss Summary:**
  - The table provides detailed statistics on the trading strategy, including the number of trades, profits, losses, and total returns.

### Exporting Results:

- **CSV Export:**
  - The app automatically saves a CSV file containing detailed segment analysis results with the filename format: `<symbol>_sma_<sma_s>_<sma_l>_<ma_type>_<start_date>_<end_date>.csv`.

### Conclusion:

Explore the results and use the information to make informed decisions about your trading strategy. Experiment with different parameters to optimize your approach.

Happy trading!

---
