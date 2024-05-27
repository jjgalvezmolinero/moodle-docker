import subprocess
import tkinter as tk
from tkinter import scrolledtext

class DockerConsole(tk.Toplevel):
    def __init__(self, parent, container_name):
        super().__init__(parent)
        self.container_name = container_name
        self.title(f"Consola de {self.container_name}")
        self.geometry('800x600')
        
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        self.text_area.configure(state='disabled')

        self.command_frame = tk.Frame(self)
        self.command_frame.pack(fill='x', padx=5, pady=5)

        self.command_entry = tk.Entry(self.command_frame)
        self.command_entry.pack(side=tk.LEFT, fill='x', expand=True)
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.bind('<Up>', self.show_previous_command)
        self.command_entry.bind('<Down>', self.show_next_command)

        self.clear_button = tk.Button(self.command_frame, text="Limpiar", command=self.clear_console)
        self.clear_button.pack(side=tk.RIGHT)

        self.command_history = []
        self.history_index = -1

    def write_output(self, output):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, output)
        self.text_area.insert(tk.END, '--------------------------------\n')
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)

    def execute_command(self, event=None):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        if command:
            self.command_history.append(command)
            self.history_index = -1
            self.write_output(f"$ {command}\n")
            try:
                result = subprocess.run(
                    ['docker', 'exec', self.container_name, 'sh', '-c', command],
                    capture_output=True, text=True
                )
                if result.stdout:
                    self.write_output(result.stdout)
                if result.stderr:
                    self.write_output(result.stderr)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

    def show_previous_command(self, event):
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            previous_command = self.command_history[-(self.history_index + 1)]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, previous_command)

    def show_next_command(self, event):
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            next_command = self.command_history[-(self.history_index + 1)]
            self.command_entry.delete(0, tk.END)
            self.command_entry.insert(0, next_command)
        elif self.command_history and self.history_index == 0:
            self.history_index -= 1
            self.command_entry.delete(0, tk.END)

    def clear_console(self):
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.configure(state='disabled')
