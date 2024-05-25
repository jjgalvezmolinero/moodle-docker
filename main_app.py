import tkinter as tk
from tkinter import messagebox, PhotoImage
import subprocess
import os
from moodle_docker_configurator import MoodleDockerConfigurator
from env_manager_gui import EnvManager
from docker_containers_checker import DockerContainersManager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main App")

        # Center the main window on the screen
        self.center_window(self.root, 300, 500)
        
        # Add logo
        self.logo = PhotoImage(file="./img/logo_negro.png")  # Change to your logo file path
        self.logo_label = tk.Label(self.root, image=self.logo)
        self.logo_label.grid(row=0, column=0, columnspan=3, pady=20)
        
        self.create_main_widgets()

    def center_window(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def create_main_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=3, pady=20)
        
        button_configurator = tk.Button(button_frame, text="Configurador de Moodle Docker", command=self.open_configurator, width=30)
        button_env_manager = tk.Button(button_frame, text="Gestión .env", command=self.open_env_manager, width=30)
        button_docker_manager = tk.Button(button_frame, text="Gestionar Docker", command=self.gestionar_docker, width=30)
        button_oracle_client = tk.Button(button_frame, text="Configurar Cliente Oracle", command=self.configurar_oracle, width=30)
        button_install_docker = tk.Button(button_frame, text="Instalar Docker", command=self.instalar_docker, width=30)
        
        button_configurator.grid(row=0, column=0, padx=10, pady=5)
        button_env_manager.grid(row=1, column=0, padx=10, pady=5)
        button_docker_manager.grid(row=2, column=0, padx=10, pady=5)
        button_oracle_client.grid(row=3, column=0, padx=10, pady=5)
        button_install_docker.grid(row=4, column=0, padx=10, pady=5)

    def open_configurator(self):
        config_window = tk.Toplevel(self.root)
        MoodleDockerConfigurator(config_window)
    
    def open_env_manager(self):
        open_window = tk.Toplevel(self.root)
        EnvManager(open_window)

    def gestionar_docker(self):
        docker_window = tk.Toplevel(self.root)
        DockerContainersManager(docker_window)

    def configurar_oracle(self):
        try:
            # Example configuration command; replace with actual commands needed for your setup
            subprocess.run(['sudo', 'cp', '-r', 'oracle', '/opt/'], check=True)
            subprocess.run(['sudo', 'apt', 'update', '&&', 'sudo', 'apt', 'install', '-y', 'libaio1'], check=True)
            os.system('sudo bash -c "echo /opt/oracle/instantclient_21_12 > /etc/ld.so.conf.d/oracle-instantclient.conf"')
            os.system('sudo ldconfig')
            messagebox.showinfo("Success", "Oracle client configured successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to configure Oracle client: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def instalar_docker(self):
        try:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'apt-transport-https', 'ca-certificates', 'curl', 'gnupg-agent', 'software-properties-common'], check=True)
            subprocess.run(['curl', '-fsSL', 'https://download.docker.com/linux/ubuntu/gpg', '|', 'sudo', 'apt-key', 'add', '-'], check=True)
            subprocess.run(['sudo', 'add-apt-repository', 'deb', '[arch=amd64]', 'https://download.docker.com/linux/ubuntu', '$(lsb_release', '-cs)', 'stable'], check=True)
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'docker-ce', 'docker-ce-cli', 'containerd.io'], check=True)
            subprocess.run(['sudo', 'usermod', '-aG', 'docker', '$USER'], check=True)
            messagebox.showinfo("Success", "Docker installed successfully. Please log out and log back in for the changes to take effect.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install Docker: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApp(root)
    root.mainloop()
