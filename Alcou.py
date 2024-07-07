import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.decomposition import PCA

class ForexAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PCA Analyzer")

        ttk.Label(self.root, text="Enter CURRENCY:").pack()
        self.ticker_entry = ttk.Entry(self.root)
        self.ticker_entry.pack()
        ttk.Button(self.root, text="Fetch Data", command=self.fetch_data).pack()

        self.eur_inr = pd.DataFrame()

        self.is_crisis_value = None
        self.pca_value = None

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def fetch_data(self):
        ticker = self.ticker_entry.get()

        try:
            self.eur_inr = yf.download(ticker, start="2006-01-01", end="2024-05-11")
        except Exception as e:
            messagebox.showinfo("No Data", f"No dataset available for {ticker}'s currency.")
            return

        self.eur_inr['Rolling_Std'] = self.eur_inr['Close'].rolling(window=30).std()

        self.crisis_threshold = 0.05  

        self.eur_inr['Is_Crisis'] = self.eur_inr['Rolling_Std'] > self.crisis_threshold

        features = self.eur_inr[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

        pca = PCA(n_components=1)
        self.eur_inr['PCA'] = pca.fit_transform(features)

        self.update_labels()
        self.update_plot()

    def update_labels(self):
        if self.is_crisis_value:
            self.is_crisis_value.destroy()
        if self.pca_value:
            self.pca_value.destroy()

        is_crisis_text = "\n".join(f"{date}: {value}" for date, value in zip(self.eur_inr.index, self.eur_inr['Is_Crisis']))
        self.is_crisis_value = tk.Text(self.root, height=10, width=50)
        self.is_crisis_value.insert(tk.END, is_crisis_text)
        self.is_crisis_value.pack()

        pca_text = "\n".join(f"{date}: {value}" for date, value in zip(self.eur_inr.index, self.eur_inr['PCA']))
        self.pca_value = tk.Text(self.root, height=10, width=50)
        self.pca_value.insert(tk.END, pca_text)
        self.pca_value.pack()

    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.eur_inr.index, self.eur_inr['Close'], label='Close Price')

        self.ax.scatter(self.eur_inr.index[self.eur_inr['Is_Crisis']], self.eur_inr.loc[self.eur_inr['Is_Crisis'], 'Close'], color='red', label='Currency Crisis')

        self.ax.axhline(y=self.crisis_threshold, color='red', linestyle='--', label='Crisis Threshold')

        self.ax.set_title('Stock Price Analysis')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Close Price')
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

def main():
    root = tk.Tk()
    app = ForexAnalyzerApp(root)
    root.mainloop()

main()
