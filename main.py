import sys
import json
import subprocess
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QMessageBox, QLineEdit, QProgressBar, QToolButton, QStatusBar,
    QGraphicsOpacityEffect
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QUrl, QTimer, QPropertyAnimation
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
    "description": "Potężny edytor graficzny do tworzenia i edycji obrazów. Obsługuje warstwy, maski i zaawansowane narzędzia edycji.",
    "icon": "https://www.gimp.org/images/frontpage/wilber-big.png",
    "install_command": "sudo zypper install -y gimp",
    "remove_command": "sudo zypper remove -y gimp",
    "check_command": "zypper se -i gimp"
  },
  {
    "name": "VLC",
    "description": "Wszechstronny odtwarzacz multimedialny obsługujący wiele formatów audio i video bez dodatkowych kodeków.",
    "icon": "https://www.videolan.org/images/logo.png",
    "install_command": "sudo zypper install -y vlc",
    "remove_command": "sudo zypper remove -y vlc",
    "check_command": "zypper se -i vlc"
  },
  {
    "name": "Firefox",
    "description": "Szybka i prywatna przeglądarka internetowa z zaawansowanymi funkcjami ochrony prywatności.",
    "icon": "https://www.mozilla.org/media/protocol/img/logos/firefox/browser/logo.eb1324e44442.svg",
    "install_command": "sudo zypper install -y firefox",
    "remove_command": "sudo zypper remove -y firefox",
    "check_command": "zypper se -i firefox"
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
        self.setObjectName("packageCard")
        self.setGraphicsEffect(QGraphicsOpacityEffect(self))  # Dla animacji fade-in

        # Główny layout karty
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Ikona z progress barem
        icon_container = QVBoxLayout()
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(64, 64)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(64, 64)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_bar.setObjectName("iconProgress")
        icon_container.addWidget(self.icon_label)
        icon_container.addWidget(self.progress_bar)
        layout.addLayout(icon_container)

        # Nazwa, opis i status
        text_layout = QVBoxLayout()
        name_layout = QHBoxLayout()
        self.name_label = QLabel(pkg["name"])
        self.name_label.setObjectName("packageName")
        self.status_label = QLabel("Zainstalowane" if self.is_installed else "Nie zainstalowane")
        self.status_label.setObjectName("statusLabel" if self.is_installed else "statusLabelNotInstalled")
        name_layout.addWidget(self.name_label)
        name_layout.addStretch()
        name_layout.addWidget(self.status_label)
        text_layout.addLayout(name_layout)
        self.desc_label = QLabel(pkg["description"])
        self.desc_label.setWordWrap(True)
        self.desc_label.setObjectName("packageDesc")
        text_layout.addWidget(self.desc_label)
        layout.addLayout(text_layout, stretch=1)

        # Przyciski z ikonami
        button_layout = QVBoxLayout()
        self.install_button = QPushButton("Zainstaluj")
        self.install_button.setIcon(QIcon.fromTheme("download"))  # Ikona pobierania
        self.install_button.setObjectName("primaryButton")
        self.install_button.setEnabled(not self.is_installed)
        self.install_button.clicked.connect(self.install_package)
        button_layout.addWidget(self.install_button)

        self.remove_button = QPushButton("Usuń")
        self.remove_button.setIcon(QIcon.fromTheme("delete"))  # Ikona usuwania
        self.remove_button.setObjectName("secondaryButton")
        self.remove_button.setEnabled(self.is_installed)
        self.remove_button.clicked.connect(self.remove_package)
        button_layout.addWidget(self.remove_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Animacja fade-in
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def load_icon(self, url):
        self.progress_bar.setVisible(True)
        self.icon_label.setVisible(False)
        manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        reply = manager.get(request)
        reply.finished.connect(lambda: self.set_icon(reply))

    def set_icon(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.icon_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.icon_label.setText("Ikona")
        self.progress_bar.setVisible(False)
        self.icon_label.setVisible(True)

    def install_package(self):
        self.install_button.setEnabled(False)
        self.install_button.setText("Instalowanie...")
        QTimer.singleShot(100, lambda: self._install_package())

    def _install_package(self):
        try:
            subprocess.run(self.pkg["install_command"], shell=True, check=True)
            self.parent().parent().parent().statusBar().showMessage(f"{self.pkg['name']} zainstalowany pomyślnie!", 5000)
            self.is_installed = True
            self.status_label.setText("Zainstalowane")
            self.status_label.setObjectName("statusLabel")
            self.install_button.setEnabled(False)
            self.install_button.setText("Zainstaluj")
            self.remove_button.setEnabled(True)
            self.style().polish(self.status_label)  # Odśwież styl
        except subprocess.CalledProcessError:
            self.parent().parent().parent().statusBar().showMessage("Błąd podczas instalacji!", 5000)
            self.install_button.setEnabled(True)
            self.install_button.setText("Zainstaluj")

    def remove_package(self):
        self.remove_button.setEnabled(False)
        self.remove_button.setText("Usuwanie...")
        QTimer.singleShot(100, lambda: self._remove_package())

    def _remove_package(self):
        try:
            subprocess.run(self.pkg["remove_command"], shell=True, check=True)
            self.parent().parent().parent().statusBar().showMessage(f"{self.pkg['name']} usunięty pomyślnie!", 5000)
            self.is_installed = False
            self.status_label.setText("Nie zainstalowane")
            self.status_label.setObjectName("statusLabelNotInstalled")
            self.install_button.setEnabled(True)
            self.remove_button.setEnabled(False)
            self.remove_button.setText("Usuń")
            self.style().polish(self.status_label)  # Odśwież styl
        except subprocess.CalledProcessError:
            self.parent().parent().parent().statusBar().showMessage("Błąd podczas usuwania!", 5000)
            self.remove_button.setEnabled(True)
            self.remove_button.setText("Usuń")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menedżer Paczek")
        self.resize(720, 480)

        # Status bar dla powiadomień (jak Snackbar w Android)
        self.setStatusBar(QStatusBar())
        self.statusBar().setObjectName("snackBar")

        # Główny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        central_widget.setLayout(layout)

        # App bar
        app_bar = QWidget()
        app_bar_layout = QHBoxLayout()
        app_bar_layout.setContentsMargins(16, 8, 16, 8)
        app_bar.setObjectName("appBar")
        title_label = QLabel("Menedżer Paczek")
        title_label.setObjectName("appBarTitle")
        app_bar_layout.addWidget(title_label)
        app_bar_layout.addStretch()
        refresh_button = QToolButton()
        refresh_button.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_button.setObjectName("appBarButton")
        refresh_button.clicked.connect(self.refresh_packages)
        app_bar_layout.addWidget(refresh_button)
        app_bar.setLayout(app_bar_layout)
        layout.addWidget(app_bar)

        # Pasek wyszukiwania
        search_container = QWidget()
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(16, 8, 16, 8)
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Szukaj paczek...")
        self.search_bar.setObjectName("searchBar")
        search_layout.addWidget(self.search_bar)
        search_container.setLayout(search_layout)
        layout.addWidget(search_container)

        # Obszar przewijany z listą paczek
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(16, 8, 16, 8)
        self.scroll_layout.setSpacing(12)
        self.scroll_content.setLayout(self.scroll_layout)

        # Wczytanie paczek i dodanie widgetów
        self.packages = load_packages()
        self.populate_packages(self.packages)

        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Filtrowanie paczek podczas wpisywania w pasku wyszukiwania
        self.search_bar.textChanged.connect(lambda text: self.filter_packages(text))

        # Floating Action Button (FAB) do dodawania nowej paczki (symulacja)
        self.fab = QPushButton("+")
        self.fab.setObjectName("fab")
        self.fab.setFixedSize(56, 56)
        self.fab.clicked.connect(lambda: self.statusBar().showMessage("Dodawanie nowej paczki (funkcja w rozwoju)", 5000))
        self.fab.setParent(self)
        self.fab.move(self.width() - 72, self.height() - 72)
        self.fab.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fab.move(self.width() - 72, self.height() - 72)

    def populate_packages(self, packages):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        for pkg in packages:
            package_widget = PackageWidget(pkg, self)
            package_widget.load_icon(pkg["icon"])
            self.scroll_layout.addWidget(package_widget)
        self.scroll_layout.addStretch()

    def filter_packages(self, text):
        filtered_packages = [pkg for pkg in self.packages if text.lower() in pkg["name"].lower() or text.lower() in pkg["description"].lower()]
        self.populate_packages(filtered_packages)

    def refresh_packages(self):
        self.packages = load_packages()
        self.populate_packages(self.packages)
        self.statusBar().showMessage("Lista odświeżona", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Wczytanie stylu QSS
    try:
        with open("style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        print("Brak pliku style.qss, używam domyślnego stylu.")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
