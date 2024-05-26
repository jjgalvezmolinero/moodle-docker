import subprocess
import json
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class DockerContainersManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contenedores Docker")
        self.root.geometry('800x600+100+100')

        # Treeview para mostrar contenedores agrupados
        self.tree = ttk.Treeview(self.root, columns=('Estado'), show='tree headings')
        self.tree.heading('#0', text='Grupo / Contenedor')
        self.tree.heading('Estado', text='Estado')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame para botones de acciones
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.refresh_button = tk.Button(self.button_frame, text="Actualizar", command=self.refresh_containers)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.button_frame, text="Iniciar Grupo", command=lambda: self.manage_group('start'))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Detener Grupo", command=lambda: self.manage_group('stop'))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.button_frame, text="Eliminar Grupo", command=lambda: self.manage_group('rm'))
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.actions_button = tk.Button(self.button_frame, text="Acciones", command=self.show_actions_menu)
        self.actions_button.pack(side=tk.LEFT, padx=5)

        # Crear el menú de acciones
        self.actions_menu = tk.Menu(self.root, tearoff=0)
        self.actions_menu.add_command(label="Habilitar phpunit", command=lambda: self.run_command_in_container('enable_phpunit'))
        self.actions_menu.add_command(label="Habilitar behat ", command=lambda: self.run_command_in_container('enable_behat'))
        self.actions_menu.add_command(label="Habilitar xdebug", command=lambda: self.run_command_in_container('enable_xdebug'))
        self.actions_menu.add_command(label="Ejecutar comando", command=lambda: self.run_command_in_container('execute_command'))
        
        # Cargar contenedores inicialmente
        self.refresh_containers()

        # Vincular el evento de clic fuera del menú para cerrarlo
        self.root.bind("<Button-1>", self.hide_actions_menu)

    def run_command_in_container(self, action):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contenedor para ejecutar el comando.")
            return

        selected_container = self.tree.item(selected_item[0], 'text')
        if not selected_container:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contenedor válido.")
            return
        
        try:
            if(action == 'enable_phpunit'):
                # Habilitamos phpunit
                command = 'php admin/tool/phpunit/cli/init.php'
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)
                # Instalamos decoradores
                command = 'php admin/tool/phpunit/cli/util.php --buildcomponentconfigs'
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)
            elif(action == 'enable_behat'):
                # Habilitamos behat
                command = 'php admin/tool/behat/cli/init.php'
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)
            elif(action == 'enable_xdebug'):
                # Pedir si la versión de php es la 7.4 o una superior
                # versionPHP = simpledialog.confirm("Versión de PHP", "¿La versión de PHP es inferior a la 8.0?")
                versionPHP = messagebox.askyesno("Versión de PHP", "¿La versión de PHP es inferior a la 8.0?")

                if versionPHP:
                    xdebug_version = 'xdebug-3.1.6'
                else:
                    xdebug_version = 'xdebug-3.3.2'

                # Habilitamos xdebug
                command = 'pecl install ' + xdebug_version
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)
                command = """
                    read -r -d '' conf <<'EOF'
                    ; Settings for Xdebug Docker configuration
                    xdebug.mode = debug
                    xdebug.client_host = host.docker.internal
                    ; Some IDEs (eg PHPSTORM, VSCODE) may require configuring an IDE key, uncomment if needed
                    ; xdebug.idekey=MY_FAV_IDE_KEY
                    EOF
                    echo '$conf' >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
                """
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)
                command = 'docker-php-ext-enable xdebug'
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)
                os.system("sudo ufw allow 9003")
                self.manage_container('restart')
            elif(action == 'execute_command'):
                command = simpledialog.askstring("Ejecutar Comando", f"Introduzca el comando para ejecutar en el contenedor {selected_container}:")
                if not command:
                    messagebox.showwarning("Advertencia", "Por favor, introduzca un comando válido.")
                    return
                subprocess.run(['docker', 'exec', selected_container] + command.split(), check=True)


            messagebox.showinfo("Éxito", f"Habilitado phpunit con éxito en el contenedor '{selected_container}'")
            self.refresh_containers()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error al ejecutar el comando '{command}' en el contenedor '{selected_container}': {e}")

    def get_docker_containers(self):
        try:
            result = subprocess.run(['docker', 'ps', '-a', '--format', '{{json .}}'], capture_output=True, text=True)
            containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
            return containers
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener contenedores de Docker: {e}")
            return []

    def group_containers(self, containers):
        grouped_containers = defaultdict(list)
        for container in containers:
            name = container['Names']
            status = container['Status']
            prefix = name.split('-')[0]
            grouped_containers[prefix].append({'name': name, 'status': status})
        return grouped_containers

    def get_group_status(self, containers):
        running = all('Up' in container['status'] for container in containers)
        stopped = all('Exited' in container['status'] for container in containers)
        if running:
            return 'green'
        elif stopped:
            return 'red'
        else:
            return 'orange'

    def refresh_containers(self):
        containers = self.get_docker_containers()
        grouped_containers = self.group_containers(containers)
        self.display_grouped_containers(grouped_containers)

    def display_grouped_containers(self, grouped_containers):
        # Limpiar items existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        for prefix, containers in grouped_containers.items():
            group_status = self.get_group_status(containers)
            group_id = self.tree.insert('', 'end', text=prefix, open=True, values=("",))
            self.tree.tag_configure(group_id, background=group_status)
            for container in containers:
                self.tree.insert(group_id, 'end', text=container['name'], values=(container['status'],))

    def manage_group(self, action):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un grupo para gestionar.")
            return

        selected_group = self.tree.item(selected_item[0], 'text')
        if not selected_group:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un grupo válido.")
            return

        containers = [self.tree.item(child)['text'] for child in self.tree.get_children(selected_item[0])]
        
        try:
            for container in containers:
                subprocess.run(['docker', action, container], check=True)
            messagebox.showinfo("Éxito", f"'{action}' ejecutado con éxito en el grupo '{selected_group}'")
            self.refresh_containers()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error al ejecutar '{action}' en el grupo '{selected_group}': {e}")

    def manage_container(self, action):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contenedor para gestionar.")
            return

        selected_container = self.tree.item(selected_item[0], 'text')
        if not selected_container:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contenedor válido.")
            return
        
        try:
            subprocess.run(['docker', action, selected_container], check=True)
            messagebox.showinfo("Éxito", f"'{action}' ejecutado con éxito en el contenedor '{selected_container}'")
            self.refresh_containers()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error al ejecutar '{action}' en el contenedor '{selected_container}': {e}")

    def show_actions_menu(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contenedor para realizar acciones.")
            return

        try:
            self.actions_menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar el menú de acciones: {e}")

    def hide_actions_menu(self, event):
        self.actions_menu.unpost()