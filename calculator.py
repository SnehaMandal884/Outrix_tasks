import tkinter as tk

def on_click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "AC":  # AC button clears everything
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)

root = tk.Tk()
root.title("Calculator with AC Button")
root.geometry("600x600")  
root.configure(bg="white")  

entry = tk.Entry(root, font=("Arial", 30), bd=5, relief=tk.SUNKEN, fg="black", bg="light yellow")
entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["AC", "0", "=", "+"]
]

colors = {
    "AC": "red",  # Red for full reset (Visible Now)
    "=": "light yellow",  # Yellow for result
    "/": "light pink", "*": "light pink", "-": "light pink", "+": "light pink",  # Pink for operators
    "default": "white"  # White for numbers
}

for row in buttons:
    row_frame = tk.Frame(frame, bg="white")
    row_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Ensure uniform spacing
    for button_text in row:
        btn_color = colors.get(button_text, colors["default"])
        button = tk.Button(row_frame, text=button_text, font=("Arial", 30), fg="black", bg=btn_color)
        button.bind("<Button-1>", on_click)
        button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

root.mainloop()
