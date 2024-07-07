import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import yfinance as yf
import pandas as pd
from sklearn.decomposition import FactorAnalysis
import matplotlib.pyplot as plt
import seaborn as sns

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

# Create a scrolled text widget for displaying the factor analysis results
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

# Function to perform factor analysis
def perform_factor_analysis():
    data = fetch_exchange_rate_data()
    if data is None:
        return
    
    # Prepare the data for factor analysis
    X = data[['USDINR=X', 'AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']]
    
    # Perform factor analysis
    fa = FactorAnalysis(n_components=2)  # Adjust the number of factors as needed
    fa.fit(X)
    
    # Display the results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Factor Loadings:\n")
   
    loadings = fa.components_.T  # Transpose to match features to factors
    for i, feature in enumerate(X.columns):
        result_text.insert(tk.END, f"{feature}: {loadings[i]}\n")
    
    # Plot the factor loadings
    plt.figure(figsize=(10, 6))
    sns.heatmap(loadings, annot=True, cmap='coolwarm', xticklabels=[f'Factor {i+1}' for i in range(loadings.shape[1])], yticklabels=X.columns)
    plt.title('Factor Loadings')
    plt.xlabel('Factors')
    plt.ylabel('Features')
    plt.show()

# Button to load and process the data
load_button = ttk.Button(frame, text="Perform Factor Analysis", command=perform_factor_analysis)
load_button.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

# Start the Tkinter event loop
root.mainloop()
