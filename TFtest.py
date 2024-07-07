import tkinter as tk
from scipy.stats import f_oneway, ttest_ind
import yfinance as yf

# Define currency pairs globally
currency_pairs = ['USDINR=X', 'AUDINR=X', 'EURINR=X', 'CHFINR=X', 'JPYINR=X']

# Function to fetch and display the exchange rate data
def fetch_exchange_rate_data():
    start_date = '2006-01-01'
    end_date = '2024-05-19'
    
    data = []
    for pair in currency_pairs:
        df = yf.download(pair, start=start_date, end=end_date)
        data.append(df['Close'])
    
    return data

# Function to calculate and display F-test results
def calculate_f_test():
    data = fetch_exchange_rate_data()
    f_statistic, p_value = f_oneway(*data)
    f_test_label.config(text=f"F-Test Results:\nF-Statistic: {f_statistic:.4f}\nP-Value: {p_value:.4e}")
    
    if p_value < 0.05:
        f_test_inference.config(text="Inference: There is a statistically significant difference between the groups.")
    else:
        f_test_inference.config(text="Inference: There is no statistically significant difference between the groups.")

# Function to calculate and display t-test results for all combinations of countries
def calculate_t_test():
    data = fetch_exchange_rate_data()
    t_test_output = ""
    significant_pairs = []
    
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            t_statistic, p_value = ttest_ind(data[i], data[j])
            t_test_output += f"\n{currency_pairs[i]} vs {currency_pairs[j]}:\nT-Stat: {t_statistic:.2f} | P-Value: {p_value:.4e}\n"
            if p_value < 0.05:
                significant_pairs.append(f"{currency_pairs[i]} vs {currency_pairs[j]}")
    
    t_test_label.config(text=t_test_output)
    
    if significant_pairs:
        t_test_inference.config(text="Inference: Statistically significant differences found between the following pairs:\n" + "\n".join(significant_pairs))
    else:
        t_test_inference.config(text="Inference: No statistically significant differences found between any pairs.")

# Create GUI
root = tk.Tk()
root.title("Statistical Tests for Exchange Rates")
root.geometry("1000x600")  # Set initial window size

# Frame for F-test
f_test_frame = tk.Frame(root)
f_test_frame.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8, anchor="nw")

# F-test button
f_test_button = tk.Button(f_test_frame, text="Perform F-Test", command=calculate_f_test)
f_test_button.pack(anchor="nw", padx=10, pady=10)

# F-test result label
f_test_label = tk.Label(f_test_frame, text="", justify=tk.LEFT, bg='lightgrey', relief='solid', padx=10, pady=10)
f_test_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# F-test inference label
f_test_inference = tk.Label(f_test_frame, text="", justify=tk.LEFT, bg='lightgrey', relief='solid', padx=10, pady=10)
f_test_inference.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame for T-test
t_test_frame = tk.Frame(root)
t_test_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.8, anchor="nw")

# T-test button
t_test_button = tk.Button(t_test_frame, text="Perform T-Test for All Country Pairs", command=calculate_t_test)
t_test_button.pack(anchor="nw", padx=10, pady=10)

# T-test result label
t_test_label = tk.Label(t_test_frame, text="", justify=tk.LEFT, bg='lightgrey', relief='solid', padx=10, pady=10, font=("Helvetica", 8))
t_test_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# T-test inference label
t_test_inference = tk.Label(t_test_frame, text="", justify=tk.LEFT, bg='lightgrey', relief='solid', padx=10, pady=10)
t_test_inference.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
