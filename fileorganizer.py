import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Define folder categories based on file extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Others": []  # Any uncategorized files
}

def organize_files(directory):
    """Organizes files in a directory into categorized folders."""
    
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Directory not found!")
        return

    # Create categorized folders if they don't exist
    for category in FILE_CATEGORIES.keys():
        category_path = os.path.join(directory, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    # Process files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Identify file type and move to respective folder
        file_extension = os.path.splitext(filename)[1].lower()
        destination_folder = "Others"

        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                destination_folder = category
                break

        # Move the file
        shutil.move(file_path, os.path.join(directory, destination_folder, filename))

    messagebox.showinfo("Success", "Files successfully organized!")

def browse_directory():
    """Opens a directory selection dialog."""
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, selected_directory)

def start_organizing():
    """Triggers file organization."""
    directory = directory_entry.get()
    if directory:
        organize_files(directory)
    else:
        messagebox.showerror("Error", "Please select a directory.")

# Setup Tkinter window
root = tk.Tk()
root.title("File Organizer Tool")
root.geometry("800x600")  # Increased window size
root.configure(bg="#f0f0f0")

tk.Label(root, text="Select a Directory to Organize:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
directory_entry = tk.Entry(root, font=("Arial", 12), width=50)
directory_entry.pack(pady=5)
browse_button = tk.Button(root, text="Browse Directory", font=("Arial", 12), bg="#ffcc00", padx=10, pady=5, command=browse_directory)
browse_button.pack(pady=10)

organize_button = tk.Button(root, text="Organize Files", font=("Arial", 14, "bold"), bg="#66ccff", padx=20, pady=10, command=start_organizing)
organize_button.pack(pady=30)

# Run the Tkinter GUI loop
root.mainloop()
