import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

# Create the main application window
root = tk.Tk()
root.title("Currency Analysis")
root.state('zoomed')  # Maximize the window

# Configure grid layout for the root window to adjust resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Set up the frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure grid layout for the frame to adjust resizing
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Create a scrolled text widget for displaying the regression results
result_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# Function to fetch and display the exchange rate data
def fetch_exchange_rate_data():
    currency_pairs = ['USDINR=X', 'AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']
    start_date = '2006-01-01'
    end_date = '2024-05-19'
    
    try:
        exchange_rate_data = yf.download(currency_pairs, start=start_date, end=end_date)['Adj Close']
        exchange_rate_data.dropna(inplace=True)
        messagebox.showinfo("Data Load", "Exchange rate data loaded successfully.")
        return exchange_rate_data
    except Exception as e:
        messagebox.showerror("Data Load Error", f"Failed to load exchange rate data: {e}")
        return None

# Function to perform polynomial regression
def perform_regression():
    data = fetch_exchange_rate_data()
    if data is None:
        return
    
    # Prepare the data for regression
    X = data[['AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']]
    y = data['USDINR=X']  # Using USDINR=X as the dependent variable
    
    # Transform the features to polynomial features
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    
    # Perform polynomial regression
    model = LinearRegression()
    model.fit(X_poly, y)
    
    # Display the results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Polynomial Regression Coefficients:\n{model.coef_}\n")
    result_text.insert(tk.END, f"Intercept: {model.intercept_}\n")
    result_text.insert(tk.END, f"R-squared: {model.score(X_poly, y)}\n")
    
    # Predict the y values
    y_pred = model.predict(X_poly)
    
    # Plot the actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.7, label='Predicted')
    
    # Add the diagonal line
    min_val = min(min(y), min(y_pred))
    max_val = max(max(y), max(y_pred))
    plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', label='Ideal')
    
    plt.xlabel('Actual INR SWAP Exchange Rate')
    plt.ylabel('Predicted INR SWAP Exchange Rate')
    plt.title('Actual vs Predicted INR SWAP Exchange Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

# Create the button to perform regression
load_button = ttk.Button(frame, text="Perform Regression", command=perform_regression)
load_button.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

root.mainloop()
