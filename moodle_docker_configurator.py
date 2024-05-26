import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

class MoodleDockerConfigurator:
    def __init__(self, root):
        self.app = root
        self.app.title('Configurador de Moodle Docker')
        self.app.geometry('400x600')
        
        # Variables de control
        self.php_version_var = tk.StringVar(value='7.4')  # Default version
        self.docker_name_var = tk.StringVar()
        self.project_name_var = tk.StringVar()
        self.app_path_var = tk.StringVar()
        self.web_host_var = tk.StringVar(value='localhost')  # Default host
        self.wwwroot_var = tk.StringVar()
        self.db_port_var = tk.StringVar()
        self.server_port_var = tk.StringVar()
        self.db_name = tk.StringVar()
        self.db_type_var = tk.StringVar(value='mysql')  # Default DB

        self.selected_env_file = None
        
        self.create_widgets()
    
    def create_widgets(self):
        entries = {
            "Versión de PHP": self.php_version_var,
            "Nombre del Proyecto": self.project_name_var,
            "Ruta de la Aplicación": self.wwwroot_var,
            "Moodle Data": self.app_path_var,
            "Host Web": self.web_host_var,
            "Nombre de la DB": self.db_name,
            "Tipo de DB": self.db_type_var,
            "Puerto de la DB": self.db_port_var,
            "Puerto del Servidor": self.server_port_var,
        }

        for label, var in entries.items():
            tk.Label(self.app, text=label+":").pack(fill='x')
            if 'Tipo' in label:
                self.create_data_base_type_select()
                continue
            entry = tk.Entry(self.app, textvariable=var)
            entry.pack(fill='x')
            if 'Ruta' in label or 'Moodle Data' in label:
                button = tk.Button(self.app, text="Buscar", command=lambda var=var: var.set(filedialog.askdirectory()))
                button.pack()

        # Botones
        tk.Button(self.app, text="Cargar Datos", command=self.cargar_datos_del_fichero).pack(fill='x')
        tk.Button(self.app, text="Guardar Configuración", command=self.save_env_variables).pack(fill='x')
        tk.Button(self.app, text="Iniciar Moodle", command=self.launch_moodle).pack(fill='x')

    def save_env_variables(self):
        env_content = (
            f"MOODLE_DOCKER_PHP_VERSION={self.php_version_var.get()}\n"
            f"COMPOSE_PROJECT_NAME={self.project_name_var.get()}\n"
            f"MOODLE_DOCKER_APP_PATH={self.app_path_var.get()}\n"
            f"MOODLE_DOCKER_WEB_HOST={self.web_host_var.get()}\n"
            f"MOODLE_DOCKER_WWWROOT={self.wwwroot_var.get()}\n"
            f"MOODLE_DOCKER_DB_PORT={self.db_port_var.get()}\n"
            f"MOODLE_DOCKER_SERVER_PORT={self.server_port_var.get()}\n"
            f"MOODLE_DOCKER_DB={self.db_type_var.get()}\n"
            f"MOODLE_DOCKER_DBNAME={self.db_name.get()}\n"
        )
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar configuración como",
            defaultextension=".env",
            filetypes=[("Env files", "*.env")]
        )
        if file_path:
            with open(file_path, 'w') as file:
                file.write(env_content)
            messagebox.showinfo("Información", f"Configuración guardada en {file_path}")

    def cargar_datos_del_fichero(self):
        self.selected_env_file = filedialog.askopenfilename(
            title="Cargar configuración",
            filetypes=[("Env files", "*.env")]
        )
        if self.selected_env_file:
            try:
                with open(self.selected_env_file, 'r') as file:
                    for line in file:
                        key, value = line.strip().split('=')
                        if key == 'MOODLE_DOCKER_PHP_VERSION':
                            self.php_version_var.set(value)
                        elif key == 'COMPOSE_PROJECT_NAME':
                            self.project_name_var.set(value)
                        elif key == 'MOODLE_DOCKER_APP_PATH':
                            self.app_path_var.set(value)
                        elif key == 'MOODLE_DOCKER_WEB_HOST':
                            self.web_host_var.set(value)
                        elif key == 'MOODLE_DOCKER_WWWROOT':
                            self.wwwroot_var.set(value)
                        elif key == 'MOODLE_DOCKER_DB_PORT':
                            self.db_port_var.set(value)
                        elif key == 'MOODLE_DOCKER_SERVER_PORT':
                            self.server_port_var.set(value)
                        elif key == 'MOODLE_DOCKER_DB':
                            self.db_type_var.set(value)
                        elif key == 'MOODLE_DOCKER_DBNAME':
                            self.docker_name_var.set(value)
            except FileNotFoundError:
                messagebox.showerror("Error", "No se ha encontrado el fichero .env")

    def launch_moodle(self):
        if self.selected_env_file:
            try:
                shutil.copyfile(self.selected_env_file, 'moodle-docker/moodle.env')
                # os.system("cd moodle-docker")
                os.system("sudo ./moodle-docker/bin/moodle-docker-compose up -d")
                messagebox.showinfo("Información", "Moodle se está iniciando...")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch Moodle: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, cargue un archivo de configuración .env antes de iniciar Moodle")

    def create_data_base_type_select(self):
        self.db_type_var.set('mysql')
        self.db_port_var.set('3306')
        self.server_port_var.set('8000')
        db_type_select = ttk.Combobox(self.app, textvariable=self.db_type_var)
        db_type_select['values'] = ('mysql', 'pgsql', 'mariadb', 'oracle')
        db_type_select.pack(fill='x')
        db_type_select.bind("<<ComboboxSelected>>", self.update_db_port)
    
    def update_db_port(self, event):
        db_type = self.db_type_var.get()
        if db_type == 'mysql':
            self.db_port_var.set('3306')
        elif db_type == 'pgsql':
            self.db_port_var.set('5432')
        elif db_type == 'mariadb':
            self.db_port_var.set('3306')
        elif db_type == 'oracle':
            self.db_port_var.set('1521')
