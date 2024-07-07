import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClusteringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Clustering Application")

        # Fit GUI to screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.label = tk.Label(root, text="Select a CSV file for clustering:")
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        self.cluster_button = tk.Button(root, text="Display Graph", command=self.display_graph)
        self.cluster_button.pack(pady=10)
        self.cluster_button.config(state=tk.DISABLED)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=20)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            self.df = pd.read_csv(file_path)

            if 'Close' not in self.df.columns or 'SMA' not in self.df.columns:
                messagebox.showerror("Error", "The required columns 'Close' and 'SMA' are not in the dataframe.")
                return
            self.cluster_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            return

    def display_graph(self):
        # Select the features for clustering
        X = self.df[['Close', 'SMA']].values

        # Standardize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply K-means clustering
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)

        # Add cluster labels to the original dataframe
        self.df['Cluster'] = clusters

        # Apply PCA for visualization (reducing to 2 dimensions)
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        # Create plot
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', edgecolor='k', s=40)
        ax.set_xlabel('CLOSE RATE')
        ax.set_ylabel('SMA PREDICTION')
        ax.set_title('K-means Clustering of Currency Data')
        fig.colorbar(scatter, ax=ax, label='Cluster')

        # Clear previous result
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Show plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=self.result_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Show dataframe head
        result_text = tk.Text(self.result_frame, height=10)
        result_text.pack(pady=10)
        result_text.insert(tk.END, self.df.head().to_string())


root = tk.Tk()
app = ClusteringApp(root)
root.mainloop()
