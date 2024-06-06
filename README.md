# Main App

Este proyecto es una aplicación de escritorio construida con Tkinter que proporciona varias funcionalidades relacionadas con la configuración y gestión de entornos Docker, así como la gestión de archivos `.env` y la configuración de Moodle Docker.

## Funcionalidades

### 1. Configurador de Moodle Docker
Permite configurar un entorno de Docker para Moodle. Abre una interfaz específica donde puedes gestionar la configuración de Moodle Docker.

### 2. Gestión `.env`
Permite gestionar archivos `.env` para diferentes entornos de desarrollo. Abre una interfaz específica para editar y gestionar variables de entorno en archivos `.env`.

### 3. Gestionar Docker
Proporciona herramientas para gestionar contenedores Docker en tu sistema. Abre una interfaz para ver, iniciar, detener y gestionar contenedores Docker.

### 4. Instalaciones
Contiene sub-funcionalidades para instalar y configurar software adicional:
- **Configurar Cliente Oracle**: Permite instalar y configurar el cliente de Oracle en el sistema.
- **Instalar Docker**: Proporciona un script para instalar Docker y Docker Compose en el sistema.

## Instalación

### Requisitos
- Python 3.10
- Tkinter
- Docker
- Acceso a internet para descargar scripts y dependencias

### Instrucciones

1. Clona el repositorio en tu máquina local:
    ```bash
    git clone https://github.com/tu_usuario/main_app.git
    cd main_app
    ```

2. Instala las dependencias necesarias:
    ```bash
    sudo pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:
    ```bash
    sudo python3 main_app.py
    ```

## Uso

Al iniciar la aplicación, verás una ventana principal con las siguientes opciones:

- **Configurador de Moodle Docker**: Haz clic en este botón para abrir el configurador de Moodle Docker.
- **Gestión `.env`**: Haz clic en este botón para abrir la gestión de archivos `.env`.
- **Gestionar Docker**: Haz clic en este botón para abrir la interfaz de gestión de Docker.
- **Instalaciones**: Haz clic en este botón para abrir una nueva ventana con las siguientes opciones:
  - **Configurar Cliente Oracle**: Haz clic en este botón para instalar y configurar el cliente Oracle.
  - **Instalar Docker**: Haz clic en este botón para instalar Docker y Docker Compose en tu sistema.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos para contribuir:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva_funcionalidad`).
3. Realiza los cambios necesarios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Envía los cambios a la rama principal (`git push origin feature/nueva_funcionalidad`).
5. Crea un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.

## Contacto

Para cualquier duda o sugerencia, puedes abrir un issue en el repositorio o contactar a los mantenedores del proyecto.

---

¡Gracias por utilizar nuestra aplicación!
