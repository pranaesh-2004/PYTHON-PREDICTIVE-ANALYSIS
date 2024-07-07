import yfinance as yf
import matplotlib.pyplot as plt

eur_inr = yf.download("EURINR=X", start="2006-01-01", end="2024-05-11")
eur_inr['Rolling_Std'] = eur_inr['Close'].rolling(window=30).std()
crisis_threshold = 0.05  
crisis_points = eur_inr[eur_inr['Rolling_Std'] > crisis_threshold]
max_date = eur_inr['Close'].idxmax()
min_date = eur_inr['Close'].idxmin()
plt.figure(figsize=(12, 6))
plt.plot(eur_inr.index, eur_inr['Close'], label='EUR/INR')
plt.scatter(crisis_points.index, crisis_points['Close'], color='red', label='Currency Crisis')
plt.axhline(y=crisis_threshold, color='red', linestyle='--', label='Crisis Threshold')
plt.annotate(f'Max: {max_date.date()}', xy=(max_date, eur_inr['Close'].loc[max_date]), 
             xytext=(max_date, eur_inr['Close'].loc[max_date] + 5),
             arrowprops=dict(facecolor='green', shrink=0.05))
plt.annotate(f'Min: {min_date.date()}', xy=(min_date, eur_inr['Close'].loc[min_date]), 
             xytext=(min_date, eur_inr['Close'].loc[min_date] - 5),
             arrowprops=dict(facecolor='blue', shrink=0.05))
plt.title('EUR/INR Exchange Rate (2006-2024)')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.legend()
plt.grid(True)
plt.show()

