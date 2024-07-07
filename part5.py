import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import yfinance as yf
import pandas as pd
from scipy.stats import ttest_ind, f_oneway

# Create the main application window
root = tk.Tk()
root.title("Currency Analysis")

# Set up the frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a scrolled text widget for displaying the test results
result_text = scrolledtext.ScrolledText(frame, width=80, height=20, wrap=tk.WORD)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Currency pairs
currency_pairs = ['USDINR=X', 'AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']

# Function to fetch and display the exchange rate data
def fetch_exchange_rate_data():
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

# Function to perform t-test and F-test
def perform_statistical_tests():
    data = fetch_exchange_rate_data()
    if data is None:
        return
    
    # Get selected currency pairs
    currency1 = currency_var1.get()
    currency2 = currency_var2.get()
    
    if currency1 == currency2:
        messagebox.showwarning("Selection Error", "Please select two different currencies.")
        return
    
    # Perform t-test
    t_stat, t_p_value = ttest_ind(data[currency1], data[currency2])
    
    # Perform F-test (ANOVA)
    f_stat, f_p_value = f_oneway(data[currency1], data[currency2])
    
    # Display the results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"T-Test between {currency1} and {currency2}:\n")
    result_text.insert(tk.END, f"t-statistic: {t_stat}\np-value: {t_p_value}\n\n")
    result_text.insert(tk.END, f"F-Test between {currency1} and {currency2}:\n")
    result_text.insert(tk.END, f"F-statistic: {f_stat}\np-value: {f_p_value}\n")

# UI elements for selecting currency pairs
currency_var1 = tk.StringVar(value=currency_pairs[0])
currency_var2 = tk.StringVar(value=currency_pairs[1])

currency_label1 = ttk.Label(frame, text="Select Currency 1:")
currency_label1.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
currency_menu1 = ttk.OptionMenu(frame, currency_var1, *currency_pairs)
currency_menu1.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

currency_label2 = ttk.Label(frame, text="Select Currency 2:")
currency_label2.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
currency_menu2 = ttk.OptionMenu(frame, currency_var2, *currency_pairs)
currency_menu2.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

# Button to perform statistical tests
test_button = ttk.Button(frame, text="Perform T-Test and F-Test", command=perform_statistical_tests)
test_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
