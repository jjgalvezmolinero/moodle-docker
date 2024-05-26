import os
import tkinter as tk
from tkinter import messagebox

class Instalaciones:
    def __init__(self, root):
        self.root = root
        self.root.title("Instalaciones")

        # Center the main window on the screen
        self.center_window(self.root, 300, 500)
        
        self.create_main_widgets()
    
    def center_window(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    
    def create_main_widgets(self):
        # Creame 2 botones para la instalación de Docker y Oracle
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=3, pady=20)

        button_oracle_client = tk.Button(button_frame, text="Configurar Cliente Oracle", command=self.configurar_oracle, width=30)
        button_install_docker = tk.Button(button_frame, text="Instalar Docker", command=self.instalar_docker, width=30)

        button_oracle_client.grid(row=0, column=0, padx=10, pady=5)
        button_install_docker.grid(row=1, column=0, padx=10, pady=5)

    def configurar_oracle(self):
        try:
            os.system('sudo rm -rf oracle')
            os.system('mkdir oracle')
            os.system('sudo apt install -y unzip')
            os.system('wget https://download.oracle.com/otn_software/linux/instantclient/2112000/el9/instantclient-basic-linux.x64-21.12.0.0.0dbru.el9.zip -O ./oracle/oracle1.zip')
            os.system('wget https://download.oracle.com/otn_software/linux/instantclient/2112000/el9/instantclient-sqlplus-linux.x64-21.12.0.0.0dbru.el9.zip -O ./oracle/oracle2.zip')
            os.system('wget https://download.oracle.com/otn_software/linux/instantclient/2112000/el9/instantclient-sdk-linux.x64-21.12.0.0.0dbru.el9.zip -O ./oracle/oracle3.zip')
            os.system('unzip ./oracle/oracle1.zip -d ./oracle/')
            os.system('unzip ./oracle/oracle2.zip -d ./oracle/')
            os.system('unzip ./oracle/oracle3.zip -d ./oracle/')
            subprocess.run(['sudo', 'cp', '-r', 'oracle', '/opt/'], check=True)
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'libaio1'], check=True)
            os.system('sudo bash -c "echo /opt/oracle/instantclient_21_12 > /etc/ld.so.conf.d/oracle-instantclient.conf"')
            os.system('sudo ldconfig')
            messagebox.showinfo("Success", "Oracle client configured successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to configure Oracle client: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def instalar_docker(self):
        try:
            os.system('curl -s https://raw.githubusercontent.com/karaage0703/ubuntu-setup/master/install-docker.sh | /bin/bash')
            os.system('sudo apt-get update')
            os.system('sudo apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common')
            os.system('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -')
            os.system('sudo apt-key fingerprint 0EBFCD88')
            os.system('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
            os.system('sudo apt-get update')
            os.system('sudo apt-get -y install docker-ce docker-ce-cli containerd.io')
            os.system('sudo apt-get -y install docker-compose-plugin')
            os.system('sudo gpasswd -a $USER docker')
            os.system('sudo systemctl enable docker')
            messagebox.showinfo("Success", "Docker installed successfully. Please log out and log back in for the changes to take effect.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install Docker: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
