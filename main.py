import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import ttk
import numpy as np

# Global variables to track current start index of displayed rows
start_index = 0
data = None  # Variable to store loaded dataset

class Table:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.total_rows = len(data)
        self.total_columns = len(data.columns)
        self.create_table()

    def create_table(self):
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=6, column=0, columnspan=4)
        
        self.tree = ttk.Treeview(self.table_frame, columns=list(self.data.columns), show='headings')
        self.tree.pack(side='left', fill='both', expand=True)
        
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        
        self.tree.configure(yscrollcommand=vsb.set)
        
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            
        for i, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

def load_dataset():
    global start_index, data, table
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        try:
            data = pd.read_csv(filename, encoding='latin1')
            info_label.config(text=f"Dataset loaded: {filename}\nShape: {data.shape}")
            start_index = 0
            display_rows()
            if table is not None:
                table.table_frame.destroy()  # Destroy previous table if exists
            table = Table(root, data)  # Create table with loaded data
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the dataset: {e}")

def display_rows():
    global start_index
    if data is not None:
        end_index = min(start_index + 10, len(data))
        subset_data = data.loc[start_index:end_index - 1, ['Youtuber', 'category', 'Title', 'Country', 'Abbreviation', 'channel_type', 'rank', 'subscribers', 'video_views_rank']]
        data_text = "Dataset:\n" + subset_data.to_string(index=False)

from scipy.stats import gaussian_kde

def visualize_histogram():
    if data is not None:
        # Convert subscribers column to numpy array
        subscribers_array = data['subscribers'].values
        
        # Example visualization: Histogram of subscribers with KDE
        plt.figure(figsize=(8, 6))
        plt.hist(subscribers_array, bins=20, density=True, alpha=0.7)
        
        # Compute KDE
        kde = gaussian_kde(subscribers_array)
        support = np.linspace(min(subscribers_array), max(subscribers_array), 100)
        plt.plot(support, kde(support), color='r', linestyle='-', linewidth=2)
        
        plt.title('Distribution of Subscribers')
        plt.xlabel('Subscribers')
        plt.ylabel('Density')
        plt.show()

def visualize_scatter():
    if data is not None:
        # Check if 'video_views' column exists in data
        if 'video_views_rank' in data.columns:
            # Example visualization: Scatter plot of subscribers vs. video views
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x='subscribers', y='video_views_rank', data=data)
            plt.title('Scatter Plot of Subscribers vs. video_views_rank')
            plt.xlabel('Subscribers')
            plt.ylabel('video_views_rank')
            plt.show()
        else:
            messagebox.showerror("Error", "Column 'video_views' does not exist in the dataset.")

def visualize_violin():
    if data is not None:
        num_categories = len(data['category'].unique())
        fig_width = min(12, num_categories * 0.8)  # Adjust the width based on the number of categories
        fig_height = min(8, num_categories * 0.6)
        plt.figure(figsize=(fig_width, fig_height))
        sns.violinplot(x='category', y='subscribers', data=data)
        plt.title('Violin Plot of Subscribers by Category')
        plt.xlabel('Category', fontsize=12)  # Adjust font size of category labels
        plt.ylabel('Subscribers')
        plt.xticks(rotation=45, ha='right')  # Rotate and align category labels
        plt.tight_layout()  # Ensure tight layout to prevent clipping
        plt.show()

# Create the main application window
root = tk.Tk()
root.title("Data Analysis Assignment by Egbunu Joshua Ukwubile")
# Set window size to full screen
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}+0+0")


# Create a button to load the dataset
load_button = tk.Button(root, text="Load Dataset", command=load_dataset)
load_button.grid(row=0, column=0, pady=10)

# Button to visualize histogram
histogram_button = tk.Button(root, text="Display Histogram", command=visualize_histogram)
histogram_button.grid(row=1, column=0)

# Button to visualize scatter plot
scatter_button = tk.Button(root, text="Display Scatter Plot", command=visualize_scatter)
scatter_button.grid(row=2, column=0)

# Button to visualize violin plot
violin_button = tk.Button(root, text="Display Violin Plot", command=visualize_violin)
violin_button.grid(row=3, column=0)

# Label to display information about the loaded dataset
info_label = tk.Label(root, text="")
info_label.grid(row=4, column=0, columnspan=2)

# Label to display rows of the dataset
data_label = tk.Label(root, text="")
data_label.grid(row=5, column=0, columnspan=2)

# Create an instance of Table
table = Table(root, pd.DataFrame())  # Create an empty table initially

# Run the tkinter event loop
root.mainloop()
