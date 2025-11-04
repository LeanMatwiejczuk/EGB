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

        # Password storage (in memory only)
        self.sudo_password = None
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        #main_frame.columnconfigure(1, weight=1)
        #main_frame.rowconfigure(2, weight=1)
        
        for i in range(8):
            main_frame.columnconfigure(i, weight=1)
        for i in range(4):
            main_frame.rowconfigure(i,weight=1)
        # Command label and entry
        ttk.Label(main_frame, text="Enter sudo command:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.command_var = tk.StringVar()
        self.command_entry = ttk.Entry(main_frame, textvariable=self.command_var)
        self.command_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        self.command_entry.bind('<Return>', self.run_command)
        
        # Run button
        self.root.run_button = ttk.Button(main_frame, text="Run Command", command=self.run_command)
        self.root.run_button.grid(row=0 , column=2, columnspan=1, padx=(5, 0), pady=(0, 5))
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        
        self.root.output_text = scrolledtext.ScrolledText(main_frame, width=50, height=20, state='disabled')
        self.root.output_text.grid(row=1, column=1,columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Clear button
        self.root.clear_button = ttk.Button(main_frame, text="Clear Output", command=self.clear_output)
        self.root.clear_button.grid(row=0 , column=3,padx=(5, 0), pady=(0, 5), sticky=tk.EW)
        
        # Set Password button
        self.root.pass_button = ttk.Button(main_frame, text="Set Sudo Password", command=self.set_password)
        self.root.pass_button.grid(row=0 , column=4,padx=(5, 0), pady=(0, 5), sticky=tk.EW)

        #Setear Setpoint button
        self.root.set_sp = ttk.Button(main_frame, text="Set Setpoint", command=self.log_command)
        self.root.set_sp.grid(row=1 , column=3 , padx=(5, 0) ,pady=(5, 0), sticky=tk.EW)

        #Check Setpoint button
        self.root.get_sp = ttk.Button(main_frame, text="Check Setpoint", command=self.log_command)
        self.root.set_sp.grid(row=1 , column=3 , padx=(5, 0) ,pady=(5, 0), sticky=tk.EW)

        #Setear Error button
        self.root.err_sp = ttk.Button(main_frame, text="Set Error", command=self.log_command)
        self.root.err_sp.grid(row=2 , column=4,padx=0,pady=0, sticky=tk.NSEW)

        #Set Mode button
        self.set_mode = ttk.Button(main_frame, text="Set Mode", command=self.log_command)
        self.set_mode.grid(row=3 , column=1, padx=(5, 0), pady=(0, 5), sticky=tk.W)

        #log button
        self.log_button = ttk.Button(main_frame, text="Log", command=self.log_command)
        self.log_button.grid(row=3 , column=2, padx=(5, 0), pady=(0, 5), sticky=tk.W)

        #Stop button
        self.stop = ttk.Button(main_frame, text="Stop", command=self.log_command)
        self.stop.grid(row=3 , column=3, padx=(5, 0), pady=(0, 5), sticky=tk.W)

        #Start button
        self.start = ttk.Button(main_frame, text="Start", command=self.log_command)
        self.start.grid(row=3 , column=4, padx=(5, 0), pady=(0, 5), sticky=tk.W)


        # Status label
        self.status_var = tk.StringVar(value="Ready - Set sudo password first")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        self.command_entry.focus()

    def set_password(self):
        """Set sudo password"""
        password = simpledialog.askstring("Sudo Password", "Enter your sudo password:", show='*', parent=self.root)
        if password:
            self.sudo_password = password
            self.status_var.set("Password set - Ready to run commands")
            messagebox.showinfo("Success", "Sudo password set successfully")

    def append_output(self, text):
        """Append text to the output area"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')

    def clear_output(self):
        """Clear the output text area"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')
        self.status_var.set("Output cleared")

    def run_command_thread(self, command):
        """Run the command in a separate thread"""
        try:
            if not self.sudo_password:
                self.append_output("Error: No sudo password set. Use 'Set Sudo Password' button first.\n")
                return
            
            self.status_var.set("Running command...")
            
            # Run the command with sudo
            process = subprocess.Popen(
                ['sudo', '-S'] + command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Provide password to sudo
            stdout, stderr = process.communicate(input=self.sudo_password + '\n')
            
            # Display output
            if stdout:
                self.append_output(f"Output:\n{stdout}\n")
            if stderr and "password" not in stderr:  # Filter out password prompt
                self.append_output(f"Errors:\n{stderr}\n")
                
            self.status_var.set(f"Command completed with return code: {process.returncode}")
            
        except Exception as e:
            self.append_output(f"Error: {str(e)}\n")
            self.status_var.set("Error occurred")
        finally:
            self.run_button.config(state='normal')
            self.command_entry.config(state='normal')

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
        self.run_button.config(state='disabled')
        self.command_entry.config(state='disabled')
        
        # Clear the command entry
        self.command_var.set("")
        
        # Run command in separate thread
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()

    def log_command(self, event=None):
        "Log command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
def main():
    root = tk.Tk()
    app = SecureSudoCommandRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()