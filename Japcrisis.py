import yfinance as yf
import matplotlib.pyplot as plt

# Fetch historical data for JPY/INR from 2006 to 2024
jpy_inr = yf.download("JPYINR=X", start="2006-01-01", end="2024-05-11")

# Calculate the rolling standard deviation to detect currency crises
jpy_inr['Rolling_Std'] = jpy_inr['Close'].rolling(window=30).std()

# Define a threshold for identifying a crisis
crisis_threshold = 0.05  # Adjust as needed

# Mark the crisis points where the rolling standard deviation exceeds the threshold
crisis_points = jpy_inr[jpy_inr['Rolling_Std'] > crisis_threshold]

# Find the dates of maximum and minimum exchange rates
max_rate_date = jpy_inr['Close'].idxmax()
min_rate_date = jpy_inr['Close'].idxmin()

# Plot JPY/INR trend
plt.figure(figsize=(12, 6))
plt.plot(jpy_inr.index, jpy_inr['Close'], label='JPY/INR')

# Mark crisis points on the plot
plt.scatter(crisis_points.index, crisis_points['Close'], color='red', label='Currency Crisis')

# Plot crisis threshold line
plt.axhline(y=crisis_threshold, color='red', linestyle='--', label='Crisis Threshold')

# Annotate maximum and minimum rate dates
plt.text(max_rate_date, jpy_inr.loc[max_rate_date, 'Close'], 'Max Rate', ha='right')
plt.text(min_rate_date, jpy_inr.loc[min_rate_date, 'Close'], 'Min Rate', ha='right')

plt.title('JPY/INR Exchange Rate (2006-2024)')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.grid(True)
plt.show()
