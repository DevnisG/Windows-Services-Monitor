" Windows Services Monitor  App"

# Libs
import os
import sys
import ctypes
from PyQt5.QtWidgets import QApplication
from gui import ServiceMonitorApp

# Func for UAC:
def run_as_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False 

# Runner
if __name__ == '__main__':
    if run_as_admin():  
        app = QApplication(sys.argv)
        app.setApplicationName("W-S-M")
        window = ServiceMonitorApp()
        window.show()
        sys.exit(app.exec_())
