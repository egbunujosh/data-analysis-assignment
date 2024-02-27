import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyperclip

# Global variables to track current start index of displayed rows
start_index = 0

def load_dataset():
    global start_index
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        # Load dataset
        global data
        data = pd.read_csv(filename)
        
        # Display basic information about the dataset
        info_label.config(text=f"Dataset loaded: {filename}\nShape: {data.shape}")
        
        # Display initial ten rows of the dataset
        start_index = 0
        display_rows()

def display_rows():
    global start_index
    if data is not None:
        end_index = min(start_index + 10, len(data))
        subset_data = data.loc[start_index:end_index - 1, ["job_link", "job_title", "company", "job_location", "search_position", "job_level", "job_type"]]
        data_text = "Dataset:\n" + subset_data.to_string(index=False)
        data_label.config(text=data_text)

def copy_link(index):
    global start_index
    if data is not None:
        job_link = data.loc[start_index + index, "job_link"]
        pyperclip.copy(job_link)

def next_rows():
    global start_index
    if start_index + 10 < len(data):
        start_index += 10
        display_rows()

def prev_rows():
    global start_index
    if start_index - 10 >= 0:
        start_index -= 10
        display_rows()

def preprocess_data(data):
    # Example preprocessing steps (replace with actual preprocessing)
    # Dropping irrelevant columns
    data = data.drop(columns=['job_link'])
    return data

def visualize_histogram():
    if data is not None:
        # Example visualization: Histogram of job levels
        plt.figure(figsize=(8, 6))
        sns.histplot(data['job_level'])
        plt.title('Distribution of Job Levels')
        plt.xlabel('Job Level')
        plt.ylabel('Frequency')
        plt.show()

def visualize_correlation():
    if data is not None:
        # Select only numeric columns
        numeric_data = data.select_dtypes(include='number')
        if not numeric_data.empty:
            # Example visualization: Correlation matrix
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Matrix')
            plt.show()
        else:
            # If there are no numeric columns, display a message
            tk.messagebox.showinfo("Error", "No numeric columns found in the dataset.")


def generate_statistics(data):
    # Example statistics (replace with actual statistics)
    description = data.describe()
    correlation = data.corr()
    return description, correlation

# Create the main application window
root = tk.Tk()
root.title("Data Analysis Assignment by Egbunu Joshua Ukwubile")

# Set window size relative to desktop size
window_width = root.winfo_screenwidth() // 2
window_height = root.winfo_screenheight() // 2
window_position_x = (root.winfo_screenwidth() - window_width) // 2
window_position_y = (root.winfo_screenheight() - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

# Create a button to load the dataset
load_button = tk.Button(root, text="Load Dataset", command=load_dataset)
load_button.pack(pady=10)

# Button to display next ten rows
next_button = tk.Button(root, text="Next", command=next_rows)
next_button.pack(side=tk.RIGHT, padx=10)

# Button to display previous ten rows
prev_button = tk.Button(root, text="Previous", command=prev_rows)
prev_button.pack(side=tk.LEFT, padx=10)

# Button to visualize histogram
histogram_button = tk.Button(root, text="Histogram", command=visualize_histogram)
histogram_button.pack()

# Button to visualize correlation
correlation_button = tk.Button(root, text="Correlation", command=visualize_correlation)
correlation_button.pack()

# Label to display information about the loaded dataset
info_label = tk.Label(root, text="")
info_label.pack()

# Label to display rows of the dataset
data_label = tk.Label(root, text="")
data_label.pack()

# Variable to store loaded dataset
data = None

# Run the tkinter event loop
root.mainloop()
