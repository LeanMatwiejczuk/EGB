# import paramiko
# import getpass

# def connect_raspberry_pi():
#     hostname = 'lse-pi4-01'
#     username = 'lse'
#     password = 'lse'
    
#     # Create SSH client
#     client = paramiko.SSHClient()
    
#     # Automatically add host key (for first-time connections)
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
#     try:
#         print(f"Connecting to {username}@{hostname}...")
        
#         # Connect to the Raspberry Pi
#         client.connect(
#             hostname=hostname,
#             username=username,
#             password=password,
#             look_for_keys=False
#         )
        
#         print("Successfully connected!")
        
#         # Example: Execute a command
#         stdin, stdout, stderr = client.exec_command('uname -a')
#         output = stdout.read().decode()
#         error = stderr.read().decode()
        
#         print(f"System info: {output}")
#         if error:
#             print(f"Error: {error}")
            
#         return client
        
#     except paramiko.AuthenticationException:
#         print("Authentication failed. Please check your credentials.")
#     except paramiko.SSHException as e:
#         print(f"SSH connection failed: {e}")
#     except Exception as e:
#         print(f"Error: {e}")
    
#     return None
# if __name__ == "__main__":
#     connect_raspberry_pi()
import tkinter as tk
from tkinter import scrolledtext, messagebox
import paramiko
import threading
import queue
import time
import re

class SSHClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH Client - Raspberry Pi")
        self.root.geometry("800x600")
        
        # SSH client
        self.ssh_client = None
        self.shell = None
        
        # Threading
        self.output_queue = queue.Queue()
        self.receiving = False
        self.waiting_for_output = False
        self.last_command = ""
        
        self.create_widgets()
        self.poll_output()
    
    def create_widgets(self):
        # Connection frame
        conn_frame = tk.Frame(self.root)
        conn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(conn_frame, text="Host:").grid(row=0, column=0, sticky="w")
        self.host_entry = tk.Entry(conn_frame, width=20)
        self.host_entry.insert(0, "lse-pi4-01")
        self.host_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(conn_frame, text="Username:").grid(row=0, column=2, padx=(20,0))
        self.user_entry = tk.Entry(conn_frame, width=15)
        self.user_entry.insert(0, "lse")
        self.user_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(conn_frame, text="Password:").grid(row=0, column=4, padx=(20,0))
        self.pass_entry = tk.Entry(conn_frame, width=15, show="*")
        self.pass_entry.insert(0, "lse")
        self.pass_entry.grid(row=0, column=5, padx=5)
        
        self.connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_ssh)
        self.connect_btn.grid(row=0, column=6, padx=20)
        
        self.disconnect_btn = tk.Button(conn_frame, text="Disconnect", command=self.disconnect_ssh, state=tk.DISABLED)
        self.disconnect_btn.grid(row=0, column=7, padx=5)
        
        # Output terminal
        tk.Label(self.root, text="Terminal Output:").pack(anchor="w", padx=10, pady=(10,0))
        
        self.output_text = scrolledtext.ScrolledText(
            self.root, 
            height=20,
            font=("Consolas", 10),
            bg='black',
            fg='white',
            insertbackground='white'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="Command:").pack(side=tk.LEFT)
        
        self.input_entry = tk.Entry(input_frame, width=60, font=("Consolas", 10))
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.bind('<Return>', self.send_command)
        self.input_entry.config(state=tk.DISABLED)
        
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_command)
        self.send_btn.pack(side=tk.LEFT, padx=5)
        self.send_btn.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Disconnected")
        status_label = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def clean_ansi_codes(self, text):
        """Remove ANSI escape sequences from text"""
        ansi_escape = re.compile(r'''
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        ''', re.VERBOSE)
        return ansi_escape.sub('', text)
    
    def clean_output(self, text, command_sent=""):
        """Clean up output and remove the echoed command"""
        # Remove ANSI codes first
        text = self.clean_ansi_codes(text)
        
        # Remove bracketed paste mode sequences
        text = text.replace('\x1b[?2004h', '')
        text = text.replace('\x1b[?2004l', '')
        
        # If we just sent a command, remove the echoed version from output
        if command_sent and self.waiting_for_output:
            # Remove the exact command echo (with or without prompt)
            patterns = [
                command_sent,  # The command itself
                f".*{re.escape(command_sent)}",  # Command with prompt
            ]
            
            for pattern in patterns:
                text = re.sub(pattern, '', text)
            
            # Reset the flag after processing
            self.waiting_for_output = False
        
        # Clean up any remaining artifacts
        text = re.sub(r'^\s*\$\s*$', '', text)  # Standalone $ prompts
        text = re.sub(r'\n+', '\n', text)  # Multiple newlines
        
        return text.strip()
    
    def connect_ssh(self):
        hostname = self.host_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not all([hostname, username, password]):
            messagebox.showerror("Error", "Please fill all connection fields")
            return
        
        # Disable connect button during connection attempt
        self.connect_btn.config(state=tk.DISABLED)
        self.status_var.set("Connecting...")
        
        # Start connection in separate thread
        thread = threading.Thread(target=self._connect_ssh_thread, args=(hostname, username, password), daemon=True)
        thread.start()
    
    def _connect_ssh_thread(self, hostname, username, password):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.ssh_client.connect(
                hostname=hostname,
                username=username,
                password=password,
                look_for_keys=False
            )
            
            # Create interactive shell
            self.shell = self.ssh_client.invoke_shell()
            self.receiving = True
            
            # Configure terminal to reduce escape codes and disable echo if possible
            self.shell.send("export TERM=xterm\n")
            time.sleep(0.5)
            self.shell.send("stty -echo\n")  # Try to disable local echo
            time.sleep(0.5)
            
            # Start receiving output in separate thread
            receive_thread = threading.Thread(target=self._receive_output, daemon=True)
            receive_thread.start()
            
            # Update UI in main thread
            self.root.after(0, self._connection_successful)
            
        except Exception as e:
            error_msg = f"Connection failed: {str(e)}"
            self.root.after(0, lambda: self._connection_failed(error_msg))
    
    def _connection_successful(self):
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.NORMAL)
        self.input_entry.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        self.status_var.set("Connected")
        
        # Clear and focus input
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()
        
        self.output_text.insert(tk.END, "=== Connected to Raspberry Pi ===\n")
        self.output_text.see(tk.END)
    
    def _connection_failed(self, error_msg):
        self.connect_btn.config(state=tk.NORMAL)
        self.status_var.set("Connection failed")
        messagebox.showerror("Connection Error", error_msg)
        self.output_text.insert(tk.END, f"Connection failed: {error_msg}\n")
    
    def _receive_output(self):
        buffer = ""
        while self.receiving and self.shell:
            try:
                if self.shell.recv_ready():
                    data = self.shell.recv(1024).decode('utf-8', errors='ignore')
                    if data:
                        buffer += data
                        
                        # Process complete lines when we have them
                        if '\n' in buffer or len(buffer) > 100:
                            # Clean the data using the last command sent
                            cleaned_data = self.clean_output(buffer, self.last_command)
                            if cleaned_data:
                                self.output_queue.put(cleaned_data + '\n')
                            buffer = ""
                            
                time.sleep(0.1)
            except:
                break
        
        # Process any remaining data in buffer
        if buffer:
            cleaned_data = self.clean_output(buffer, self.last_command)
            if cleaned_data:
                self.output_queue.put(cleaned_data + '\n')
    
    def send_command(self, event=None):
        if not self.shell:
            return
        
        command = self.input_entry.get().strip()
        if not command:
            return
        
        # Store the command and set flag
        self.last_command = command
        self.waiting_for_output = True
        
        # Add newline to execute command
        full_command = command + '\n'
        
        try:
            # Show the command we're sending (only once)
            self.output_text.insert(tk.END, f"$ {command}\n")
            self.output_text.see(tk.END)
            
            # Send the command
            self.shell.send(full_command)
            self.input_entry.delete(0, tk.END)
            
        except Exception as e:
            self.output_text.insert(tk.END, f"Error sending command: {str(e)}\n")
            self.output_text.see(tk.END)
            self.waiting_for_output = False
    
    def poll_output(self):
        try:
            while True:
                output = self.output_queue.get_nowait()
                # Only add output if it's not empty after cleaning
                if output.strip():
                    self.output_text.insert(tk.END, output)
                    self.output_text.see(tk.END)
        except queue.Empty:
            pass
        
        self.root.after(100, self.poll_output)
    
    def disconnect_ssh(self):
        self.receiving = False
        
        if self.shell:
            self.shell.close()
        if self.ssh_client:
            self.ssh_client.close()
        
        self.connect_btn.config(state=tk.NORMAL)
        self.disconnect_btn.config(state=tk.DISABLED)
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.status_var.set("Disconnected")
        
        self.output_text.insert(tk.END, "\n=== Disconnected ===\n")
        self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SSHClientGUI(root)
    root.mainloop()