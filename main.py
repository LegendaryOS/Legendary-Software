import sys
import json
import subprocess
import os
import urllib.request
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QMessageBox, QFrame
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

# Funkcja do wczytania danych o paczkach z pliku JSON
def load_packages():
    try:
        with open("packages.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [
            {
                "name": "GIMP",
                "description": "Potężny edytor graficzny.",
                "icon": "https://www.gimp.org/images/frontpage/wilber-big.png",
                "install_command": "sudo zypper install -y gimp",
                "remove_command": "sudo zypper remove -y gimp",
                "check_command": "zypper se -i gimp"
            },
            {
                "name": "VLC",
                "description": "Odtwarzacz multimedialny.",
                "icon": "https://www.videolan.org/images/logo.png",
                "install_command": "sudo zypper install -y vlc",
                "remove_command": "sudo zypper remove -y vlc",
                "check_command": "zypper se -i vlc"
            }
        ]

# Funkcja sprawdzająca, czy paczka jest zainstalowana
def is_package_installed(check_command):
    try:
        result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
        return result.returncode == 0 and result.stdout.strip() != ""
    except subprocess.CalledProcessError:
        return False

class PackageWidget(QWidget):
    def __init__(self, pkg, parent=None):
        super().__init__(parent)
        self.pkg = pkg
        self.is_installed = is_package_installed(pkg["check_command"])

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Ikona
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(50, 50)
        self.load_icon(pkg["icon"])
        layout.addWidget(self.icon_label)

        # Nazwa i opis
        text_layout = QVBoxLayout()
        self.name_label = QLabel(pkg["name"])
        self.name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.desc_label = QLabel(pkg["description"])
        self.desc_label.setWordWrap(True)
        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.desc_label)
        layout.addLayout(text_layout, stretch=1)

        # Przyciski
        self.install_button = QPushButton("Zainstaluj")
        self.install_button.setEnabled(not self.is_installed)
        self.install_button.clicked.connect(self.install_package)
        layout.addWidget(self.install_button)

        self.remove_button = QPushButton("Usuń")
        self.remove_button.setEnabled(self.is_installed)
        self.remove_button.clicked.connect(self.remove_package)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: white; border-bottom: 1px solid #ddd;")

    def load_icon(self, url):
        manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        reply = manager.get(request)
        reply.finished.connect(lambda: self.set_icon(reply))

    def set_icon(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.icon_label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.icon_label.setText("Ikona")

    def install_package(self):
        try:
            subprocess.run(self.pkg["install_command"], shell=True, check=True)
            QMessageBox.information(self, "Sukces", "Paczka zainstalowana pomyślnie!")
            self.is_installed = True
            self.install_button.setEnabled(False)
            self.remove_button.setEnabled(True)
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "Błąd", "Błąd podczas instalacji!")

    def remove_package(self):
        try:
            subprocess.run(self.pkg["remove_command"], shell=True, check=True)
            QMessageBox.information(self, "Sukces", "Paczka usunięta pomyślnie!")
            self.is_installed = False
            self.install_button.setEnabled(True)
            self.remove_button.setEnabled(False)
        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "Błąd", "Błąd podczas usuwania!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menedżer Paczek")
        self.resize(600, 400)

        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)

        # Nagłówek
        header = QLabel("Menedżer Paczek")
        header.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px; background-color: #2196F3; color: white;")
        layout.addWidget(header)

        # Obszar przewijany z listą paczek
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        scroll_content.setLayout(scroll_layout)

        # Wczytanie paczek i dodanie widgetów
        packages = load_packages()
        for pkg in packages:
            package_widget = PackageWidget(pkg)
            scroll_layout.addWidget(package_widget)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Wczytanie stylu QSS
    try:
        with open("style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        pass  # Jeśli plik nie istnieje, użyj domyślnego stylu
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
