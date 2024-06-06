import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class EnvManager:
    def __init__(self, root):
        self.app = root
        self.app.title('Gestor de Archivos .env')
        self.app.geometry('700x600')
        self.directory = './variables'
        self.env_files = self.get_env_files()
        self.selected_file_path = tk.StringVar()
        self.file_content = tk.Text(self.app)       
        
        self.create_widgets()

    def copy_config_file(self):        
        content = self.file_content.get(1.0, tk.END)
        # Buscar la línea que contiene MOODLE_DOCKER_WWWROOT
        lines = content.splitlines()
        ruta_proyecto = ''
        for line in lines:
            if line.startswith("MOODLE_DOCKER_WWWROOT"):
                ruta_proyecto = line.split("=", 1)[1]
                continue
        if not ruta_proyecto:
            messagebox.showerror("Error", "No se encontró la variable MOODLE_DOCKER_WWWROOT en el archivo seleccionado.")
            return
        
        example_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'moodle-docker/config.docker-template.php')
        destination = os.path.join(ruta_proyecto, 'config.php')

        if not os.path.exists(ruta_proyecto):
            messagebox.showerror("Error", "No existe la ruta del proyecto "+ruta_proyecto)
            return
        
        if shutil.copy(example_config_path, destination):
            messagebox.showinfo("Éxito", "Archivo config.php copiado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo copiar el archivo config.php.")

    def create_widgets(self):
        tk.Label(self.app, text="Archivos .env en las carpetas:").pack(fill='x')
        
        self.tree = ttk.Treeview(self.app)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_file_select)

        self.populate_tree()

        button_frame = tk.Frame(self.app)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Cargar Archivo", command=self.load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Guardar Cambios", command=self.save_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Duplicar Archivo", command=self.duplicate_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Lanzar Archivo", command=self.launch_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Copiar config", command=self.copy_config_file).pack(side=tk.LEFT, padx=5)
        
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
            node_path = selection[0]
            self.selected_file_path.set(self.get_full_path(node_path))
            self.load_file()

    def get_full_path(self, node_path):
        parts = node_path.split('/')
        current_path = self.directory
        for part in parts:
            current_path = os.path.join(current_path, part)
        return current_path

    def load_file(self):
        file_path = self.selected_file_path.get()
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                self.file_content.delete(1.0, tk.END)
                self.file_content.insert(tk.END, content)

    def save_file(self):
        file_path = self.selected_file_path.get()
        if os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                content = self.file_content.get(1.0, tk.END)
                file.write(content.strip())
            messagebox.showinfo("Información", "Archivo guardado correctamente.")

    def duplicate_file(self):
        file_path = self.selected_file_path.get()
        if os.path.isfile(file_path):
            new_file_path = filedialog.asksaveasfilename(title="Guardar copia como", defaultextension=".env", filetypes=[("Env files", "*.env")])
            if new_file_path:
                shutil.copyfile(file_path, new_file_path)
                self.env_files.append(new_file_path)
                self.populate_tree()
                messagebox.showinfo("Información", "Archivo duplicado correctamente.")

    def launch_file(self):
        file_path = self.selected_file_path.get()
        if os.path.isfile(file_path):
            shutil.copyfile(file_path, './moodle-docker/moodle.env')
            try:
                subprocess.run(['sudo', './moodle-docker/bin/moodle-docker-compose', 'up', '-d'], check=True)
                messagebox.showinfo("Información", f"{os.path.basename(file_path)} se está ejecutando...")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to launch: {e}")