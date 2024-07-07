import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Create the main application window
root = tk.Tk()
root.title("Currency Analysis")
root.state('zoomed')  # Maximize the window

# Set up the frame
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Create a scrolled text widget for displaying the regression results
result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Function to fetch and display the exchange rate data
def fetch_exchange_rate_data():
    currency_pairs = ['USDINR=X', 'AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']
    start_date = '2006-01-01'
    end_date = '2012-12-31'
    
    try:
        exchange_rate_data = yf.download(currency_pairs, start=start_date, end=end_date)['Adj Close']
        exchange_rate_data.dropna(inplace=True)
        messagebox.showinfo("Data Load", "Exchange rate data loaded successfully.")
        return exchange_rate_data
    except Exception as e:
        messagebox.showerror("Data Load Error", f"Failed to load exchange rate data: {e}")
        return None

# Function to perform multiple linear regression
def perform_regression():
    data = fetch_exchange_rate_data()
    if data is None:
        return
    
    # Prepare the data for regression
    X = data[['AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']]
    y = data['USDINR=X']  # Using USDINR=X as the dependent variable
    
    # Perform multiple linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Display the results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Regression Coefficients:\n{model.coef_}\n")
    result_text.insert(tk.END, f"Intercept: {model.intercept_}\n")
    result_text.insert(tk.END, f"R-squared: {model.score(X, y)}\n")
    
    # Plot the actual vs predicted values
    y_pred = model.predict(X)
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.7)
    
    # Add the diagonal line
    min_val = min(min(y), min(y_pred))
    max_val = max(max(y), max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='Ideal')
    
    plt.xlabel('Actual INR Exchange Rate')
    plt.ylabel('Predicted INR Exchange Rate')
    plt.title('Actual vs Predicted INR Exchange Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

# Button to load and process the data
load_button = ttk.Button(frame, text="Perform Regression", command=perform_regression)
load_button.pack(padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
