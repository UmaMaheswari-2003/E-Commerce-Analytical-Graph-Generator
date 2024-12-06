import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def import_csv():
    """Import data from a CSV file."""
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", ".csv"), ("All files", ".*")]
    )
    if file_path:
        try:
            # Read the CSV file
            data = pd.read_csv(file_path)
            # Display column options
            columns = list(data.columns)
            if len(columns) < 2:
                result_label.config(text="Error: CSV must have at least two columns")
                return

            x_dropdown["values"] = columns
            y_dropdown["values"] = columns
            result_label.config(text="CSV loaded successfully! Select columns for X and Y.")
            global csv_data
            csv_data = data
        except Exception as e:
            result_label.config(text=f"Error reading CSV: {e}")

def plot_from_csv():
    """Plot the graph using selected CSV columns."""
    try:
        # Get selected columns
        x_column = x_dropdown.get()
        y_column = y_dropdown.get()
        if not x_column or not y_column:
            result_label.config(text="Error: Select X and Y columns")
            return

        # Extract data
        x_values = csv_data[x_column].dropna().tolist()
        y_values = csv_data[y_column].dropna().tolist()

        # Clear existing plots
        fig.clear()

        # Create a bar graph
        ax = fig.add_subplot(111)
        ax.bar(x_values, y_values, color='b', label=f'{x_column} vs {y_column}')
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title('Analytical Graph')
        ax.legend()
        ax.grid(True)

        # Redraw the canvas
        canvas.draw()
        result_label.config(text="Bar graph plotted successfully!")
    except Exception as e:
        result_label.config(text=f"Error plotting graph: {e}")

# Create main Tkinter window
root = tk.Tk()
root.title("CSV Bar Graph Plotter")

# Main frame to hold widgets
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="NSEW")

# Configure grid weights for resizing
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.columnconfigure(0, weight=1)

# Input frame for CSV import and column selection
input_frame = ttk.Frame(main_frame, padding="10")
input_frame.grid(row=0, column=0, sticky="EW", pady=5)

ttk.Button(input_frame, text="Import CSV", command=import_csv).grid(row=0, column=0, padx=5)

ttk.Label(input_frame, text="X Column:").grid(row=1, column=0, sticky="W")
x_dropdown = ttk.Combobox(input_frame, state="readonly", width=30)
x_dropdown.grid(row=1, column=1, padx=5)

ttk.Label(input_frame, text="Y Column:").grid(row=2, column=0, sticky="W")
y_dropdown = ttk.Combobox(input_frame, state="readonly", width=30)
y_dropdown.grid(row=2, column=1, padx=5)

ttk.Button(input_frame, text="Plot Graph", command=plot_from_csv).grid(row=3, column=0, columnspan=2, pady=10)

# Result label
result_label = ttk.Label(main_frame, text="", foreground="red")
result_label.grid(row=1, column=0, pady=5)

# Frame for the graph
graph_frame = ttk.Frame(main_frame, padding="10")
graph_frame.grid(row=2, column=0, sticky="NSEW")

# Configure graph_frame to expand
graph_frame.rowconfigure(0, weight=1)
graph_frame.columnconfigure(0, weight=1)

# Matplotlib Figure and Canvas
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, sticky="NSEW")

# Global variable to hold CSV data
csv_data = None

# Start Tkinter event loop
root.mainloop()
