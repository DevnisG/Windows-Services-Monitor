# Libs
import os
import json

# Func for get resources path (assets):
def get_resource_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

# Func for create and run pw_shell scripts:
def create_powershell_script(service_file):
    services_data = load_services(service_file)
    services_running = services_data.get('running', [])
    services_stopping = services_data.get('stopping', [])

    script_lines = []

    # Starting Services:
    for service in services_running:
        script_lines.append(
            f"if ((Get-Service -Name '{service}').Status -ne 'Running') {{ Start-Service '{service}'; Write-Host 'Servicio {service} iniciado.' }} else {{ Write-Host 'Servicio {service} ya está corriendo.' }}"
        )

    # Stopping Services:
    for service in services_stopping:
        script_lines.append(
            f"if ((Get-Service -Name '{service}').Status -eq 'Running') {{ Stop-Service '{service}'; Write-Host 'Servicio {service} detenido.' }}"
        )

    script_content = '; '.join(script_lines)
    return f'while ($true) {{ {script_content}; Start-Sleep -Seconds 30 }}'

# Func for load the services from json file:
def load_services(service_file):
    if os.path.exists(service_file):
        with open(service_file, 'r') as file:
            return json.load(file)
    return {
        'stop_services': [],
        'run_services': []
    }

# Func for save the services from ui into json file:
def save_services(service_file, services):
    with open(service_file, 'w') as file:
        json.dump(services, file)