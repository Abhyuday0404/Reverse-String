import socket
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from docx import Document

HOST = '127.0.0.1'
PORT = 65432

def send_string_to_server(message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(message.encode())
            data = s.recv(1024)
            return data.decode()
    except Exception as e:
        return f"Error: {e}"

def reverse_input_string():
    user_input = entry.get()
    if not user_input:
        messagebox.showwarning("Input Required", "Please enter a string.")
        return
    reversed_str = send_string_to_server(user_input)
    result_label.config(text=reversed_str)

def load_file():
    filepath = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )
    if not filepath:
        messagebox.showinfo("Info", "No file was selected")
        return
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if not content:
                messagebox.showwarning("Warning", "The selected file is empty")
                return
            entry.delete(0, tk.END)
            entry.insert(0, content)
            messagebox.showinfo("Success", f"File loaded successfully: {filepath}")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "The selected file is not a valid text file")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {str(e)}")

def save_reversed_text():
    reversed_text = result_label.cget("text")
    if not reversed_text or reversed_text.isspace():
        messagebox.showwarning("Warning", "No reversed text to save!")
        return
        
    filepath = filedialog.asksaveasfilename(
        title="Save Reversed Text",
        filetypes=[("Text files", "*.txt")],
        defaultextension=".txt"
    )
    
    if not filepath:
        return
        
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(reversed_text)
        messagebox.showinfo("Success", f"File saved successfully as {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def clear_text():
    entry.delete(0, tk.END)
    result_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("String Reversal Client")

# Set window size and position it in center
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.configure(bg='#f0f0f0')  # Light gray background

# Connection Info Frame
conn_frame = tk.Frame(root, bg='#f0f0f0', padx=10, pady=5)
conn_frame.pack(fill=tk.X)
tk.Label(
    conn_frame,
    text=f"Host: {HOST}",
    font=('Helvetica', 10),
    bg='#f0f0f0',
    fg='#666666'
).pack(side=tk.LEFT, padx=(0, 15))
tk.Label(
    conn_frame,
    text=f"Port: {PORT}",
    font=('Helvetica', 10),
    bg='#f0f0f0',
    fg='#666666'
).pack(side=tk.LEFT)

# Title Frame
title_frame = tk.Frame(root, bg='#2c3e50', pady=15)  # Dark blue background
title_frame.pack(fill=tk.X)

title_label = tk.Label(
    title_frame,
    text="String Reversal Application",
    font=('Helvetica', 16, 'bold'),
    bg='#2c3e50',
    fg='white'
)
title_label.pack()

# Main Content Frame
content_frame = tk.Frame(root, bg='#f0f0f0', padx=20)
content_frame.pack(expand=True, fill=tk.BOTH, pady=20)

# Input Frame
input_frame = tk.Frame(content_frame, bg='#f0f0f0')
input_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(
    input_frame,
    text="Enter text or load from file:",
    font=('Helvetica', 10),
    bg='#f0f0f0'
).pack(pady=(0, 5))

entry = tk.Entry(input_frame, width=50, font=('Helvetica', 14))
entry.pack(fill=tk.X, pady=(0, 10), ipady=5)

# Button Frame
btn_frame = tk.Frame(content_frame, bg='#f0f0f0')
btn_frame.pack(pady=10)

button_style = {
    'font': ('Helvetica', 10),
    'width': 15,
    'pady': 5,
    'cursor': 'hand2'
}

reverse_btn = tk.Button(
    btn_frame,
    text="Reverse String",
    command=reverse_input_string,
    bg='#ADD8E6',  # Light blue
    fg='black',
    **button_style
)
reverse_btn.pack(side=tk.LEFT, padx=5)

load_btn = tk.Button(
    btn_frame,
    text="Load from File",
    command=load_file,
    bg='#ADD8E6',  # Light blue
    fg='black',
    **button_style
)
load_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(
    btn_frame,
    text="Save Reversed Text",
    command=save_reversed_text,
    bg='#ADD8E6',  # Light blue
    fg='black',
    **button_style
)
save_btn.pack(side=tk.LEFT, padx=5)

clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    command=clear_text,
    bg='#808080',  # Grey
    fg='white',
    **button_style
)
clear_btn.pack(side=tk.LEFT, padx=5)

# Result Frame
result_frame = tk.Frame(content_frame, bg='#f0f0f0')
result_frame.pack(fill=tk.X, pady=20)

# Label for "Reversed:" text
tk.Label(
    result_frame,
    text="Reversed:",
    font=('Helvetica', 14, 'bold'),
    bg='#f0f0f0'
).pack(pady=(0, 5))

# Label for the actual reversed text
result_label = tk.Label(
    result_frame,
    text="",
    font=('Helvetica', 14),
    bg='#ffffff',  # White background
    wraplength=550,  # Allow text to wrap
    relief=tk.SUNKEN,  # Add a sunken border effect
    padx=10,
    pady=10,
    width=40,
    height=3
)
result_label.pack(fill=tk.X)

# Add hover effects for buttons
def on_enter(e):
    e.widget['bg'] = {
        'Reverse String': '#87CEEB',  # Slightly darker light blue
        'Load from File': '#87CEEB',  # Slightly darker light blue
        'Save Reversed Text': '#87CEEB',  # Slightly darker light blue
        'Clear': '#696969'  # Darker grey
    }[e.widget['text']]

def on_leave(e):
    e.widget['bg'] = {
        'Reverse String': '#ADD8E6',  # Light blue
        'Load from File': '#ADD8E6',  # Light blue
        'Save Reversed Text': '#ADD8E6',  # Light blue
        'Clear': '#808080'  # Grey
    }[e.widget['text']]

for btn in [reverse_btn, load_btn, save_btn, clear_btn]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root.mainloop()
