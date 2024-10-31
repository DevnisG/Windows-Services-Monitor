# Libs
import os
import json
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QProcess
from config import LIGHT_THEME, DARK_THEME
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QMessageBox, QSystemTrayIcon, QDialog, QTextEdit, 
                             QMenu, QAction, QSpacerItem, QSizePolicy,
                             QApplication)
from utils import get_resource_path, create_powershell_script, load_services, save_services

# Main Class UI:
class ServiceMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = False 
        self.process = None
        self.service_file = 'services.json'
        self.init_ui() 

    # Init UI Func:
    def init_ui(self):
        self.setWindowTitle('W-S-M')
        self.setWindowIcon(QIcon(get_resource_path('assets/icon.png')))
        self.setFixedSize(400, 320)
        self.layout = QVBoxLayout()
        self.banner_label = self.add_banner()
        self.add_buttons()
        self.setLayout(self.layout)
        self.center()
        self.create_tray_icon()
        self.apply_theme(LIGHT_THEME)

    # Func for add banner:
    def add_banner(self):
        banner_label = QLabel(self)
        banner_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(banner_label)
        return banner_label 

    # Func for Add Buttons:
    def add_buttons(self):
        start_button = QPushButton('Iniciar Monitoreo', self)
        start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(start_button)

        stop_button = QPushButton('Detener Monitoreo', self)
        stop_button.clicked.connect(self.stop_monitoring)
        self.layout.addWidget(stop_button)

        config_button = QPushButton('Agregar Servicios', self)
        config_button.clicked.connect(self.configure_services)
        self.layout.addWidget(config_button)

        self.theme_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.theme_layout.addItem(spacer)
        self.theme_button = QPushButton(self)
        self.theme_button.setIcon(QIcon(get_resource_path('assets/dark.png')))
        self.theme_button.setFixedSize(50, 50) 
        self.theme_button.clicked.connect(self.toggle_theme)
        self.theme_layout.addWidget(self.theme_button)
        self.layout.addLayout(self.theme_layout)
        self.update_theme_button_icon()

    # Func for update theme mode:
    def update_theme_button_icon(self):
        if self.is_dark_mode:
            self.theme_button.setIcon(QIcon(get_resource_path('assets/light.png')))
        else:
            self.theme_button.setIcon(QIcon(get_resource_path('assets/dark.png')))

    # Func for open the app into middle of the screen:
    def center(self):
        screen_geom = QApplication.primaryScreen().geometry()
        size = self.size()
        x = (screen_geom.width() - size.width()) // 2
        y = (screen_geom.height() - size.height()) // 2
        self.move(x, y)

    # Func for Start the monitoring of services:
    def start_monitoring(self):
        if not os.path.exists(self.service_file):
            QMessageBox.warning(self, 'Error', 'El archivo de servicios no existe.')
            return

        self.stop_monitoring()  
        self.process = QProcess(self)
        self.process.setProgram('cmd.exe')
        self.process.setArguments(['/c', 'powershell', '-Command', create_powershell_script(self.service_file)])
        self.process.start()
        QMessageBox.information(self, 'Monitoreo', 'Monitoreo iniciado.')

    # Func for Stop the monitoring of services:
    def stop_monitoring(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished()
            QMessageBox.information(self, 'Monitoreo', 'Monitoreo detenido.')

    # Func for Configure the monitoring of services:
    def configure_services(self):
        services = load_services(self.service_file)
        stop_services_text = '\n'.join(services.get('stop_services', []))
        run_services_text = '\n'.join(services.get('run_services', []))
        
        dialog = QDialog(self)
        dialog.setWindowTitle('Configuración de Servicios')
        dialog.setFixedSize(400, 320)
        layout = QVBoxLayout()
        
        stop_services_label = QLabel('Servicios a Mantener Detenidos:', dialog)
        layout.addWidget(stop_services_label)
        stop_text_edit = QTextEdit(dialog)
        stop_text_edit.setPlainText(stop_services_text) 
        layout.addWidget(stop_text_edit)

        run_services_label = QLabel('Servicios a Mantener Encendidos:', dialog)
        layout.addWidget(run_services_label)
        run_text_edit = QTextEdit(dialog)
        run_text_edit.setPlainText(run_services_text) 
        layout.addWidget(run_text_edit)

        save_button = QPushButton('Agregar Servicios e Iniciar Monitoreo', dialog)
        save_button.clicked.connect(lambda: self.save_services(stop_text_edit.toPlainText(), run_text_edit.toPlainText(), dialog))
        layout.addWidget(save_button)
        
        dialog.setLayout(layout)
        dialog.exec_()

    # Func for save services into app:
    def save_services(self, stop_services_text, run_services_text, dialog):
        services_data = {
            'stop_services': stop_services_text.splitlines(),
            'run_services': run_services_text.splitlines()
        }
        
        save_services(self.service_file, services_data)
        QMessageBox.information(self, 'Configuración', 'La configuración ha sido guardada.')
        dialog.accept()

    # Func for create a persistence in Windows Notch:
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Windows Services Monitor",
            "La aplicación se sigue ejecutando para mantener los servicios activos.",
            QSystemTrayIcon.Information,
            2000
        )

    # Func for create a Icon in Windows notch:
    def create_tray_icon(self):
        tray_icon = QSystemTrayIcon(self)
        tray_icon.setIcon(QIcon(get_resource_path('assets/icon.png')))
        tray_menu = QMenu(self)

        open_action = QAction('Mostrar', self)
        open_action.triggered.connect(self.show_app)
        tray_menu.addAction(open_action)

        start_action = QAction('Iniciar Monitoreo', self)
        start_action.triggered.connect(self.start_monitoring)
        tray_menu.addAction(start_action)

        stop_action = QAction('Detener Monitoreo', self)
        stop_action.triggered.connect(self.stop_monitoring)
        tray_menu.addAction(stop_action)

        config_action = QAction('Configuración', self)
        config_action.triggered.connect(self.configure_services)
        tray_menu.addAction(config_action)

        exit_action = QAction('Salir', self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()
        self.tray_icon = tray_icon

    # Func for show app from notch:
    def show_app(self):
        self.show()
        self.raise_()
        self.activateWindow()

    # Func for close app from notch:
    def exit_app(self):
        self.stop_monitoring()
        QApplication.instance().quit()

    # Func for toggle theme mode:
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        theme = DARK_THEME if self.is_dark_mode else LIGHT_THEME
        self.apply_theme(theme)
        self.update_theme_button_icon()

    # Func for apply theme:
    def apply_theme(self, theme):
        self.setStyleSheet(theme.get('app_style', ''))
        for child in self.findChildren(QPushButton):
            child.setStyleSheet(theme.get('button_style', ''))
        for child in self.findChildren(QLabel):
            if child != self.banner_label:
                child.setStyleSheet(theme.get('label_style', ''))  
        banner_image = 'assets/banner_dark.png' if self.is_dark_mode else 'assets/banner_white.png'
        self.banner_label.setPixmap(QPixmap(get_resource_path(banner_image)))

