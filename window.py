import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import subprocess
import threading
import sys
import os
import time

class SecureSudoCommandRunner:
    def __init__(self, root0):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.root = root0
        self.root.title("Uart Command Runner")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        self.root.resizable(False,False)

        # Password storage (in memory only)
        self.sudo_password = None

        # Configure grid weights
        #self.root.columnconfigure(0, weight=1)
        #self.root.rowconfigure(0, weight=1)
        #main_frame.columnconfigure(1, weight=1)
        #main_frame.rowconfigure(2, weight=1)
        
        for i in range(8):
            self.root.columnconfigure(i, weight=1)
        for i in range(3):
            self.root.rowconfigure(i,weight=1)
        
        # Create run files button
        self.create_run_files= ttk.Button(self.root, text="Create Run Files", command=self.create_files_command)
        self.create_run_files.grid(row=0, column=0, sticky=tk.NSEW, pady=5, padx=5)
        
        # Insmod Button
        self.ins_files= ttk.Button(self.root, text="Insert Run Files", command=self.ins_files_command)
        self.ins_files.grid(row=0, column=1, sticky=tk.NSEW, pady=5, padx=5)
        
        # Delete Files button
        self.run_button = ttk.Button(self.root, text="Delete Run Files", command=self.del_files_command)
        self.run_button.grid(row=0 , column=2, padx=5, pady=5, sticky= tk.NSEW)
        
        # Clear button
        self.clear_button = ttk.Button(self.root, text="Clear Output", command=self.clear_output)
        self.clear_button.grid(row=0 , column=3, padx=5, pady=5, sticky= tk.NSEW)
        
        # Set Password button
        self.pass_button = ttk.Button(self.root, text="Set Sudo Password", command=self.set_password)
        self.pass_button.grid(row=0 , column=4, padx=5, pady=5, sticky= tk.NSEW)
        
        # DEBUG LS BUTTON
        self.pass_button = ttk.Button(self.root, text="LS", command=self.debug)
        self.pass_button.grid(row=0 , column=5, padx=5, pady=5, sticky= tk.NSEW)

        # Output text area
        label2=ttk.Label(self.root, text="Output:")
        label2.grid(row=1, column=0, sticky=tk.EW, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=10, state='disabled')
        self.output_text.grid(row=1, column=1, sticky=tk.NSEW, pady=5, padx=5)
        
        #Setear Setpoint button
        self.set_sp = ttk.Button(self.root, text="Set Setpoint", command=self.set_sp_command)
        self.set_sp.grid(row=1 , column=2, padx=5, pady=5, sticky= tk.NSEW)

        #Check Setpoint button
        self.get_sp = ttk.Button(self.root, text="Check Setpoint", command=self.get_sp_command)
        self.get_sp.grid(row=1 , column=3, padx=5, pady=5, sticky= tk.NSEW)

        #Setear Error button
        self.set_err = ttk.Button(self.root, text="Set Error", command=self.set_err_command)
        self.set_err.grid(row=1 , column=4, padx=5, pady=5, sticky= tk.NSEW)

        #Get Error button
        self.get_err = ttk.Button(self.root, text="Get Error", command=self.get_err_command)
        self.get_err.grid(row=1 , column=5, padx=5, pady=5, sticky= tk.NSEW)

        #log button
        self.log_button = ttk.Button(self.root, text="Log", command=self.log_command)
        self.log_button.grid(row=2 , column=2, padx=5, pady=5, sticky= tk.NSEW)

        #Stop button
        self.stop = ttk.Button(self.root, text="Stop", command=self.stop_command)
        self.stop.grid(row=2 , column=3, padx=5, pady=5, sticky= tk.NSEW)

        #Start button
        self.start = ttk.Button(self.root, text="Start", command=self.start_command)
        self.start.grid(row=2 , column=4, padx=5, pady=10, sticky= tk.NSEW)
        
        #Set Mode button
        self.set_mode = ttk.Button(self.root, text="Set Mode", command=self.set_mode_command)
        self.set_mode.grid(row=2 , column=5 ,padx=5, pady=10,  sticky=tk.NSEW)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready - Set sudo password first")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)
        
        #self.command_entry.focus()

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
        self.run_button.config(state='enabled')
        self.command_entry.config(state='enabled')

    def create_files_command(self, event=None):
        # "Runs Makefile"
        # if not self.sudo_password:
        #     messagebox.showwarning("Warning", "Please set sudo password first")
        #     return
        # if os.path.isdir('build'):
        #     main_command = 'make clean'
        #     echo_command = 'echo "DELETING BUILD FOLDER \n"'
        # else:
        #     main_command = 'make all'
        #     echo_command = 'echo "CREATING BUILD FOLDER \n"'

        # def run_echo_main():
        #     self.append_output(f"$ sudo {echo_command}\n")
        #     self.run_command_thread(echo_command)

        #     self.append_output(f"$ sudo {main_command}\n")
        #     self.run_command_thread(main_command)

        # # Run the command
        # main_thread = threading.Thread(target=run_echo_main)
        # main_thread.daemon = True
        # main_thread.start()
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
        if os.path.isdir('build'):
            messagebox.showwarning("Warning", "BUILD FOLDER ALREADY EXISTS")
            return
        command = "make all"
        self.append_output(f"$ sudo {command}\n")
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()
        time.sleep(5)
        messagebox.showwarning("", "BUILD FOLDER CREATED")
        #self.clear_output()

    def debug(self, event=None):
        "DEBUG - USA LS"
        command = "ls"
        self.append_output(f"${command}\n")
    
        # Run the command
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()



    def ins_files_command(self,event=None):
        "Runs Insmod or Rmmod"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
        command = "rmmod build/dev_uart.ko"
        self.append_output(f"$ sudo {command}\n")
    
        # Run the command
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()

        command = "insmod build/dev_uart.ko"
        self.append_output(f"$ sudo {command}\n")
    
        # Run the command
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()

    def del_files_command(self,event=None):
        "Runs Make Clean"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
        if not os.path.isdir('build'):
            messagebox.showwarning("Warning", "BUILD FOLDER DOES NOT EXIST")
            return
        command = "make clean"
        self.append_output(f"$ sudo {command}\n")
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()
        time.sleep(5)
        messagebox.showwarning("", "BUILD FOLDER DELETED")


    def set_sp_command(self, event=None):
        "Set Setpoint command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return

    def get_sp_command(self, event=None):
        "Check Setpoint command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
    
    def get_err_command(self, event=None):
        "Get Error command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return

    def set_err_command(self, event=None):
        "Set Error command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
    
    def set_mode_command(self, event=None):
        "Set Mode command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return

    def log_command(self, event=None):
        "Log command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
    
    def stop_command(self, event=None):
        "Stop command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
        
    def start_command(self, event=None):
        "Start command"
        if not self.sudo_password:
            messagebox.showwarning("Warning", "Please set sudo password first")
            return
        
        command = "ls -al" 
        self.append_output(f"$ sudo {command}\n")
    
        # Run the command
        thread = threading.Thread(target=self.run_command_thread, args=(command,))
        thread.daemon = True
        thread.start()
        
def main():
    root = tk.Tk()
    app = SecureSudoCommandRunner(root)
    root.mainloop()

if __name__ == "__main__":
    main()