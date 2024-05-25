import subprocess
import json
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox

class DockerContainersManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de contenedores Docker")
        self.root.geometry('800x600')

        # Treeview for displaying grouped containers
        self.tree = ttk.Treeview(self.root, columns=('Estado'), show='tree headings')
        self.tree.heading('#0', text='Grupo /Contenedor')
        self.tree.heading('Estado', text='Estado')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame for action buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.refresh_button = tk.Button(self.button_frame, text="Actualizar", command=self.refresh_containers)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.button_frame, text="Iniciar grupo", command=lambda: self.manage_group('start'))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Detener grupo", command=lambda: self.manage_group('stop'))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Quitar grupo", command=lambda: self.manage_group('rm'))
        self.remove_button.pack(side=tk.LEFT, padx=5)

        # Initial load of containers
        self.refresh_containers()

    def get_docker_containers(self):
        try:
            result = subprocess.run(['docker', 'ps', '-a', '--format', '{{json .}}'], capture_output=True, text=True)
            containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
            return containers
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener contenedores Docker: {e}")
            return []

    def group_containers(self, containers):
        grouped_containers = defaultdict(list)
        for container in containers:
            name = container['Names']
            status = container['Status']
            prefix = name.split('-')[0]
            grouped_containers[prefix].append({'name': name, 'status': status})
        return grouped_containers

    def refresh_containers(self):
        containers = self.get_docker_containers()
        grouped_containers = self.group_containers(containers)
        self.display_grouped_containers(grouped_containers)

    def display_grouped_containers(self, grouped_containers):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        for prefix, containers in grouped_containers.items():
            group_id = self.tree.insert('', 'end', text=prefix, open=True)
            for container in containers:
                self.tree.insert(group_id, 'end', text=container['name'], values=(container['status'],))

    def manage_group(self, action):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor seleccione un grupo para administrar.")
            return

        selected_group = self.tree.item(selected_item[0], 'text')
        if not selected_group:
            messagebox.showwarning("Advertencia", "Por favor seleccione un grupo válido.")
            return

        containers = [self.tree.item(child)['text'] for child in self.tree.get_children(selected_item[0])]
        
        try:
            for container in containers:
                subprocess.run(['docker', action, container], check=True)
            messagebox.showinfo("Éxito", f"Ejecutado con éxito'{action}' en grupo '{selected_group}'")
            self.refresh_containers()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo ejecutar '{action}' en grupo '{selected_group}': {e}")
