import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import subprocess
import threading
import sys

class SecureSudoCommandRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("Uart Command Runner")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        self.root.resizable(False,False)
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        
        self.sudo_password = None
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        for i in range(8):
            main_frame.columnconfigure(i, weight=1)
        for i in range(4):
            main_frame.rowconfigure(i,weight=1)
        
        ttk.Label(main_frame, text="Enter sudo command:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(main_frame, textvariable=self.command_var)
        self.command_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5))
        self.command_entry.bind('<Return>', self.run_command)
        
        # Run button
        self.root.run_button = ttk.Button(main_frame, text="Run Command", command=self.run_command)
        self.root.run_button.grid(row=0 , column=2)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        
        self.root.output_text = scrolledtext.ScrolledText(main_frame, width=20, height=20, state='disabled')
        self.root.output_text.grid(row=1, column=1, columnspan=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        for row in range(3):
            for col in range(8):
                btn = ttk.Button(main_frame, text=f"R{row+1}C{col}")
                btn.grid(row=row+1, column=col, sticky=tk.EW, padx=1, pady=1)

    def run_command(self, event=None):
        """Execute the sudo command"""
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
            
        command = self.command_var.get().strip()
        
        if not command:
            messagebox.showwarning("Warning", "Please enter a command")
            return
        
        # Show the command in output
        self.append_output(f"$ sudo {command}\n")
        
        # Disable controls while running
        #self.run_button.config(state='disabled')
        self.command_entry.config(state='disabled')
        
        # Clear the command entry
        self.command_var.set("")
        
        # Run command in separate thread
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = SecureSudoCommandRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()