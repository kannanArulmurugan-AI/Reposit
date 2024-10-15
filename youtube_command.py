# import tkinter as tk
# from tkinter import messagebox, ttk
# import subprocess
# import threading
# import re

# # Globallist to keep track of processes
# processes = []

# def update_progress(process, progress_bar, percentage_label):
#     """
#     Function to update the progress bar based on yt-dlp output.
#     """
#     for line in process.stdout:
#         line = line.decode('utf-8').strip()
#         # Extract the percentage from yt-dlp output (e.g., "50.0%")
#         match = re.search(r"(\d{1,3}\.\d)%", line)
#         if match:
#             percentage = float(match.group(1))
#             progress_bar['value'] = percentage  # Update the progress bar
#             percentage_label.config(text=f"{percentage:.1f}%")  # Update percentage label

# def execute_command(url, entry, button, cancel_button, process_index, progress_bar, percentage_label):
#     if not url:
#         messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
#         return

#     # Concatenate the static command with the YouTube URL
#     command = f"yt-dlp -f best --external-downloader aria2c --external-downloader-args '-x 10 -s 10 -j 10 --max-tries=99 --retry-wait=5 ' {url}"

#     try:
#         # Start the process using Popen and capture stdout for progress updates
#         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         processes[process_index] = process  # Store the process object for cancellation

#         # Start a thread to update the progress bar based on the yt-dlp output
#         threading.Thread(target=update_progress, args=(process, progress_bar, percentage_label)).start()

#         # Wait for the process to complete
#         process.wait()
        
#         # Remove the widgets once the process completes
#         entry.destroy()
#         button.destroy()
#         cancel_button.destroy()
#         progress_bar.destroy()
#         percentage_label.destroy()

#     except subprocess.CalledProcessError as e:
#         messagebox.showerror("Execution Error", f"An error occurred: {e}")

# def cancel_command(process_index, entry, button, cancel_button, progress_bar, percentage_label):
#     # Terminate the process
#     process = processes[process_index]
#     if process.poll() is None:  # Check if the process is still running
#         process.terminate()
#         messagebox.showinfo("Process Terminated", "The process has been terminated.")
    
#     # Clean up the widgets
#     entry.destroy()
#     button.destroy()
#     cancel_button.destroy()
#     progress_bar.destroy()
#     percentage_label.destroy()

# def create_command():
#     row = len(root.grid_slaves()) // 3  # Get the current row to arrange new widgets

#     # Create a new textbox for the URL
#     new_entry = tk.Entry(root, width=50, font=('Arial', 12))
#     new_entry.grid(row=row + 2, column=0, padx=10, pady=5, sticky='ew')

#     # Create an index for the current process
#     process_index = len(processes)
#     processes.append(None)  # Placeholder for the process

#     # Create the "Execute Command" button
#     new_button = tk.Button(root, text="Execute", font=('Arial', 10), bg="#4CAF50", fg="white", 
#                            command=lambda: threading.Thread(target=execute_command, args=(new_entry.get(), new_entry, new_button, cancel_button, process_index, progress_bar, percentage_label)).start())
#     new_button.grid(row=row + 2, column=1, padx=10, pady=5)

#     # Create a "Cancel" button
#     cancel_button = tk.Button(root, text="Cancel", font=('Arial', 10), bg="#f44336", fg="white", 
#                               command=lambda: cancel_command(process_index, new_entry, new_button, cancel_button, progress_bar, percentage_label))
#     cancel_button.grid(row=row + 2, column=2, padx=10, pady=5)

#     # Create a progress bar
#     progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
#     progress_bar.grid(row=row + 3, column=0, padx=10, pady=5, columnspan=2, sticky='ew')

#     # Create a label to display percentage
#     percentage_label = tk.Label(root, text="0.0%", font=('Arial', 10))
#     percentage_label.grid(row=row + 3, column=2, padx=10, pady=5, sticky='w')

# # Create the main window
# root = tk.Tk()
# root.title("YouTube URL Command Executor")

# # Set a fixed window size and background color
# root.geometry('700x500')
# root.configure(bg="#f0f0f0")

# # Place the "Add" button at the top-left corner
# add_button = tk.Button(root, text="Add URL", font=('Arial', 12), bg="#008CBA", fg="white", command=create_command)
# add_button.grid(row=1, column=0, padx=10, pady=5, sticky='nw')

# # Make the columns resizable
# root.grid_columnconfigure(0, weight=1)

# # Run the application
# root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

# Global list to keep track of processes and URLs
processes = []
urls_from_sheet = []

# Function to fetch URLs from Google Sheet
def fetch_urls_from_google_sheet():
    global urls_from_sheet
    # Set up Google Sheets API credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Open the sheet and fetch the URLs from the first column
    sheet = client.open("YourGoogleSheetName").sheet1  # Replace with your Google Sheet name
    urls_from_sheet = sheet.col_values(1)  # Assuming URLs are in the first column

def update_progress(process, progress_bar, percentage_label):
    """
    Function to update the progress bar based on yt-dlp output.
    """
    for line in process.stdout:
        line = line.decode('utf-8').strip()
        # Extract the percentage from yt-dlp output (e.g., "50.0%")
        match = re.search(r"(\d{1,3}\.\d)%", line)
        if match:
            percentage = float(match.group(1))
            progress_bar['value'] = percentage  # Update the progress bar
            percentage_label.config(text=f"{percentage:.1f}%")  # Update percentage label

def execute_command(urls, entry, button, cancel_button, process_index, progress_bar, percentage_label):
    if not urls:
        messagebox.showwarning("Input Error", "No URLs to process.")
        return

    # Construct the download command for two URLs at once
    command = f"yt-dlp -f best --external-downloader aria2c --external-downloader-args '-x 10 -s 10 -j 10 --max-tries=99 --retry-wait=5 ' {urls[0]} {urls[1]}"
    
    try:
        # Start the process using Popen and capture stdout for progress updates
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        processes[process_index] = process  # Store the process object for cancellation

        # Start a thread to update the progress bar based on the yt-dlp output
        threading.Thread(target=update_progress, args=(process, progress_bar, percentage_label)).start()

        # Wait for the process to complete
        process.wait()
        
        # Remove the widgets once the process completes
        entry.destroy()
        button.destroy()
        cancel_button.destroy()
        progress_bar.destroy()
        percentage_label.destroy()

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Execution Error", f"An error occurred: {e}")

def cancel_command(process_index, entry, button, cancel_button, progress_bar, percentage_label):
    # Terminate the process
    process = processes[process_index]
    if process.poll() is None:  # Check if the process is still running
        process.terminate()
        messagebox.showinfo("Process Terminated", "The process has been terminated.")
    
    # Clean up the widgets
    entry.destroy()
    button.destroy()
    cancel_button.destroy()
    progress_bar.destroy()
    percentage_label.destroy()

def create_command(from_google_sheet):
    global urls_from_sheet

    row = len(root.grid_slaves()) // 3  # Get the current row to arrange new widgets

    if from_google_sheet.get():
        # Fetch URLs from Google Sheet if checkbox is checked
        if not urls_from_sheet:
            fetch_urls_from_google_sheet()
        urls = urls_from_sheet[:2]  # Get two URLs from the list
        urls_from_sheet = urls_from_sheet[2:]  # Remove the processed URLs from the list
        url_text = f"{urls[0]}, {urls[1]}"
    else:
        url_text = "Manually Entered"  # Text for manual entries

    # Create a new label to display the URLs
    new_entry = tk.Label(root, text=url_text, font=('Arial', 12))
    new_entry.grid(row=row + 2, column=0, padx=10, pady=5, sticky='ew')

    # Create an index for the current process
    process_index = len(processes)
    processes.append(None)  # Placeholder for the process

    # Create the "Execute Command" button
    new_button = tk.Button(root, text="Execute", font=('Arial', 10), bg="#4CAF50", fg="white", 
                           command=lambda: threading.Thread(target=execute_command, args=(urls_from_sheet[:2], new_entry, new_button, cancel_button, process_index, progress_bar, percentage_label)).start())
    new_button.grid(row=row + 2, column=1, padx=10, pady=5)

    # Create a "Cancel" button
    cancel_button = tk.Button(root, text="Cancel", font=('Arial', 10), bg="#f44336", fg="white", 
                              command=lambda: cancel_command(process_index, new_entry, new_button, cancel_button, progress_bar, percentage_label))
    cancel_button.grid(row=row + 2, column=2, padx=10, pady=5)

    # Create a progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode='determinate')
    progress_bar.grid(row=row + 3, column=0, padx=10, pady=5, columnspan=2, sticky='ew')

    # Create a label to display percentage
    percentage_label = tk.Label(root, text="0.0%", font=('Arial', 10))
    percentage_label.grid(row=row + 3, column=2, padx=10, pady=5, sticky='w')

# Create the main window
root = tk.Tk()
root.title("YouTube URL Command Executor")

# Set a fixed window size and background color
root.geometry('700x500')
root.configure(bg="#f0f0f0")

# Checkbox to choose whether to fetch from Google Sheet
from_google_sheet = tk.BooleanVar()
checkbox = tk.Checkbutton(root, text="From Google Sheet", variable=from_google_sheet, font=('Arial', 12), bg="#f0f0f0")
checkbox.grid(row=0, column=0, padx=10, pady=5, sticky='nw')

# Place the "Add URL" button at the top-left corner
add_button = tk.Button(root, text="Add URL", font=('Arial', 12), bg="#008CBA", fg="white", command=lambda: create_command(from_google_sheet))
add_button.grid(row=1, column=0, padx=10, pady=5, sticky='nw')

# Make the columns resizable
root.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
