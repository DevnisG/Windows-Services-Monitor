Windows Services Monitor App es una herramienta de código abierto diseñada para gestionar y monitorear servicios en sistemas Windows. Esta aplicación permite a los usuarios controlar de manera eficiente los servicios del sistema a través de una interfaz gráfica intuitiva.

1. ¿Qué es Windows Services Monitor App y para qué sirve?

Este proyecto permite:

- Monitoreo de Servicios: Iniciar y detener el monitoreo de servicios de Windows, asegurando que ciertos servicios estén en ejecución y que otros se detengan.

- Configuración de Servicios: Agregar servicios a una lista de ejecución o detención, guardando estas configuraciones en un archivo JSON.

- Interfaz Gráfica Intuitiva: Facilita la gestión de servicios sin necesidad de usar la línea de comandos, todo desde una única aplicación.

- Soporte para Modo Claro y Oscuro: Cambia la apariencia de la aplicación según la preferencia del usuario.

Es especialmente útil para administradores de sistemas y usuarios que necesitan supervisar y controlar servicios en máquinas Windows de forma sencilla.

2. ¿Cómo se utiliza?
Iniciar la aplicación: Al abrirla, se solicita permiso de administrador (es necesario para gestionar servicios de Windows).

Configurar Servicios:

- Haz clic en "Agregar Servicios" para definir qué servicios deseas que estén en ejecución o detenidos.

- Guarda la configuración y cierra el diálogo.
  
- Iniciar Monitoreo: Haz clic en "Iniciar Monitoreo" para comenzar a supervisar los servicios según la configuración establecida.

- Detener Monitoreo: Puedes detener el monitoreo en cualquier momento haciendo clic en "Detener Monitoreo".

3. ¿Cómo se compila?
Para compilar el proyecto y crear un archivo ejecutable (.exe) para distribución, sigue estos pasos:

Clona el repositorio: git clone https://github.com/tu_usuario/windows-services-monitor.git

Accede al directorio del proyecto: cd windows-services-monitor

Instala las dependencias: pip install -r requirements.txt

Ejecuta la aplicación: python main.py

Crear .EXE para despliegue en producción
Para generar un archivo ejecutable (.exe) de Windows Services Monitor App y facilitar su distribución como una aplicación independiente, ejecuta el siguiente comando:

Comandos:

pyinstaller --onefile --windowed --icon="icon.png" --add-data "assets;assets" main.py

Este comando compilará el proyecto en un ejecutable de Windows, ideal para entornos de producción.

NOTA:
Esta aplicación requiere permisos de administrador para funcionar correctamente, ya que necesita acceso para iniciar y detener servicios de Windows.

![Screenshot 2024-10-31 074914](https://github.com/user-attachments/assets/5ee76794-2d36-41ee-b1a0-2f5a76c43906)



