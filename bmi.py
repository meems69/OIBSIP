import tkinter as tk
from tkinter import messagebox
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime 

def calculate_bmi(weight, height):
    try:
        height_meters = height / 100.0 
        bmi = weight / (height_meters ** 2)
        return bmi
    except ZeroDivisionError:
        messagebox.showerror("Error", "Height cannot be zero!")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 24.9 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_bmi_data(data, date):
    filename = "bmi_data.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    data["date"] = date

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)

def plot_bmi_trend():
    filename = "bmi_data.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            bmi_data = json.load(file)
            
            dates = []
            bmis = []
            
            for entry in bmi_data:
                if "date" in entry and "bmi" in entry:
                    dates.append(entry["date"])
                    bmis.append(entry["bmi"])

            if dates and bmis:  # Check if there's data to plot
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(dates, bmis, marker='o', linestyle='-')
                ax.set_xlabel('Date')
                ax.set_ylabel('BMI')
                ax.set_title('BMI Trend Over Time')
                ax.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()

                plot_window = tk.Toplevel()
                plot_window.title("BMI Trend Analysis")
                plot_canvas = FigureCanvasTkAgg(fig, master=plot_window)
                plot_canvas.get_tk_widget().pack()
                plot_canvas.draw()
            else:
                messagebox.showinfo("Information", "No BMI data available.")
    else:
        messagebox.showinfo("Information", "No BMI data available.")

root = tk.Tk()
root.title("BMI Calculator")

label_weight = tk.Label(root, text="Enter Weight (kg):")
entry_weight = tk.Entry(root)

label_height = tk.Label(root, text="Enter Height (cm):")
entry_height = tk.Entry(root)

result_label = tk.Label(root, text="BMI Result:")

def calculate_button_clicked():
    weight = float(entry_weight.get())
    height = float(entry_height.get())
    bmi = calculate_bmi(weight, height)
    if bmi:
        result_label.config(text=f"BMI: {bmi:.2f} ({classify_bmi(bmi)})")

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "classification": classify_bmi(bmi),
        }
        save_bmi_data(data, current_date)

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_button_clicked)

plot_button = tk.Button(root, text="Plot BMI Trend", command=plot_bmi_trend)

label_weight.grid(row=0, column=0)
entry_weight.grid(row=0, column=1)
label_height.grid(row=1, column=0)
entry_height.grid(row=1, column=1)
calculate_button.grid(row=2, column=0, columnspan=2)
result_label.grid(row=3, column=0, columnspan=2)
plot_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
