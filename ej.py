import tkinter as tk
from tkinter import ttk, scrolledtext

def create_grid_window():
    root = tk.Tk()
    root.title("Grid Layout Example")
    root.geometry("800x600")
    
    # Configure grid weights for resizing
    for i in range(8):
        root.columnconfigure(i, weight=1)
    for i in range(4):
        root.rowconfigure(i, weight=1)
    
    # Row 0
    # [0,0] - Label
    label1 = ttk.Label(root, text="Label 1")
    label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    # [0,1] - Text box
    text_box = tk.Text(root, height=2, width=20)
    text_box.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    # [0,2], [0,3], [0,4] - Buttons
    button1 = ttk.Button(root, text="Button 1", command=lambda: print("Button 1"))
    button1.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    
    button2 = ttk.Button(root, text="Button 2", command=lambda: print("Button 2"))
    button2.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
    
    button3 = ttk.Button(root, text="Button 3", command=lambda: print("Button 3"))
    button3.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
    
    # Row 1
    # [1,0] - Label
    label2 = ttk.Label(root, text="Output:")
    label2.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    
    # [1,1] - ScrolledText
    scrolled_text = scrolledtext.ScrolledText(root, height=10, width=40)
    scrolled_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    
    # Fill remaining cells with buttons
    button_count = 1
    for row in range(4):
        for col in range(8):
            # Skip cells that already have widgets
            if (row == 0 and col in [0, 1, 2, 3, 4]) or (row == 1 and col in [0, 1]):
                continue
                
            btn = ttk.Button(root, text=f"Btn {button_count}", 
                           command=lambda bc=button_count: print(f"Button {bc}"))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            button_count += 1
    
    root.mainloop()

if __name__ == "__main__":
    create_grid_window()