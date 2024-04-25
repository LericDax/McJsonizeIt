import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Button, Label, Progressbar, Entry
import json
import os

# Function to get a unique output file name based on input
def get_unique_output_filename(input_file, output_folder):
    base_name = os.path.basename(input_file)
    base_name_no_ext = os.path.splitext(base_name)[0]
    output_file = os.path.join(output_folder, f"{base_name_no_ext}.jsonl")

    # If file exists, generate a unique name
    counter = 1
    while os.path.exists(output_file):
        output_file = os.path.join(output_folder, f"{base_name_no_ext}_{counter}.jsonl")
        counter += 1

    return output_file


# Function to convert JSON to JSONL with a progress bar update
def convert_json_to_jsonl(input_file, output_file, progress):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        with open(output_file, 'w') as f:
            if isinstance(data, list):
                total_items = len(data)
                for index, item in enumerate(data):
                    f.write(json.dumps(item) + '\n')
                    progress['value'] = (index + 1) / total_items * 100
                    progress.update_idletasks()
            else:
                f.write(json.dumps(data) + '\n')
                progress['value'] = 100
                progress.update_idletasks()

        return output_file
    except Exception as e:
        messagebox.showerror("Conversion Error", f"An error occurred during conversion: {e}")
        return None


# Create a simple style with a bright tropical theme
app = Style(theme='solar')  # Bright theme with tropical colors
root = app.master
root.title("Tropical JSON to JSONL Converter")

# Main frame for layout
main_frame = Frame(root, padding=20, style='primary.TFrame')  # Caribbean cerulean background
main_frame.pack(pady=10, padx=10, fill='both', expand=True)

# Function to select an input JSON file
def select_input_file():
    file = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=[("JSON files", "*.json")]
    )
    input_entry.delete(0, 'end')
    input_entry.insert(0, file)


# Function to select the output folder
def select_output_folder():
    folder = filedialog.askdirectory(
        title="Select Output Folder"
    )
    output_entry.delete(0, 'end')
    output_entry.insert(0, folder)


# Convert function
def on_convert():
    input_file = input_entry.get()
    output_folder = output_entry.get()

    if not os.path.isfile(input_file):
        messagebox.showwarning("Invalid Input", "Please select a valid JSON file.")
        return

    if not os.path.isdir(output_folder):
        messagebox.showwarning("Invalid Output Folder", "Please select a valid output folder.")
        return

    progress_bar['value'] = 0
    output_file = get_unique_output_filename(input_file, output_folder)

    converted_file = convert_json_to_jsonl(input_file, output_file, progress_bar)

    if converted_file:
        messagebox.showinfo("Conversion Success", f"Converted and saved to {converted_file}.")


# Create the layout with tropical-themed widgets
input_label = Label(main_frame, text="Select Input JSON File:", style='info.TLabel')  # Sea blue
input_label.pack(pady=5, anchor='w')

input_entry = Entry(main_frame, width=50, style='info.TEntry')  # Sea blue
input_entry.pack(pady=5, padx=5, fill='x', expand=True)

input_button = Button(main_frame, text="Browse", command=select_input_file, style='success.TButton')  # Tropical green
input_button.pack(pady=5, anchor='w')

output_label = Label(main_frame, text="Select Output Folder:", style='info.TLabel')  # Sea blue
output_label.pack(pady=5, anchor='w')

output_entry = Entry(main_frame, width=50, style='info.TEntry')  # Sea blue
output_entry.pack(pady=5, padx=5, fill='x', expand=True)

output_button = Button(main_frame, text="Browse", command=select_output_folder, style='success.TButton')  # Tropical green
output_button.pack(pady=5, anchor='w')

convert_button = Button(main_frame, text="Convert JSON to JSONL", command=on_convert, style='warning.TButton')  # Orange
convert_button.pack(pady=10)

progress_label = Label(main_frame, text="Conversion Progress:", style='primary.TLabel')  # Blue
progress_label.pack(pady=5, anchor='w')

progress_bar = Progressbar(main_frame, length=200, mode='determinate', style='info.TProgressbar')  # Blue
progress_bar.pack(pady=10, fill='x')

# Start the event loop
root.mainloop()
