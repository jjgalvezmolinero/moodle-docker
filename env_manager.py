import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class EnvManager:
    def __init__(self, root):
        self.app = root
        self.app.title('Gestor de Archivos .env')
        self.app.geometry('800x600+100+100')
        self.directory = './variables'
        self.env_files = self.get_env_files()
        self.selected_file = tk.StringVar()
        self.file_content = tk.Text(self.app)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.app, text="Archivos .env en las carpetas:").pack(fill='x')
        
        self.tree = ttk.Treeview(self.app)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_file_select)

        self.populate_tree()

        tk.Button(self.app, text="Cargar Archivo", command=self.load_file).pack(fill='x')
        tk.Button(self.app, text="Guardar Cambios", command=self.save_file).pack(fill='x')
        tk.Button(self.app, text="Lanzar Archivo", command=self.launch_file).pack(fill='x')
        
        tk.Label(self.app, text="Contenido del archivo:").pack(fill='x')
        self.file_content.pack(fill='both', expand=True)

    def get_env_files(self):
        env_files = []
        for root, dirs, files in os.walk(self.directory):
            env_files.extend([os.path.join(root, file) for file in files if file.endswith('.env')])
        return env_files

    def populate_tree(self):
        for file_path in self.env_files:
            relative_path = os.path.relpath(file_path, self.directory)
            parts = relative_path.split(os.sep)
            parent = ''
            for part in parts:
                if parent:
                    node = f"{parent}/{part}"
                else:
                    node = part
                if not self.tree.exists(node):
                    self.tree.insert(parent, 'end', node, text=part)
                parent = node

    def on_file_select(self, event):
        selection = event.widget.selection()
        if selection:
            self.selected_file.set(self.tree.item(selection[0], 'text'))
            self.load_file()

    def load_file(self):
        selected_item = self.tree.selection()[0]
        file_path = os.path.join(self.directory, self.tree.item(selected_item, 'text'))
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                self.file_content.delete(1.0, tk.END)
                self.file_content.insert(tk.END, content)

    def save_file(self):
        selected_item = self.tree.selection()[0]
        file_path = os.path.join(self.directory, self.tree.item(selected_item, 'text'))
        if os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                content = self.file_content.get(1.0, tk.END)
                file.write(content.strip())
            messagebox.showinfo("Información", "Archivo guardado correctamente.")

    def launch_file(self):
        selected_item = self.tree.selection()[0]
        file_path = os.path.join(self.directory, self.tree.item(selected_item, 'text'))
        if os.path.isfile(file_path):
            os.system(f"source {file_path}")
            messagebox.showinfo("Información", f"{self.tree.item(selected_item, 'text')} se está ejecutando...")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvManager(root)
    root.mainloop()
