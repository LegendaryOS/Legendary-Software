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
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "packages.json")
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: 'packages.json' not found at {json_path}. Loading default package list.")
        return [
  {
    "name": "GIMP",
    "description": "Potężny edytor graficzny do tworzenia i edycji obrazów. Obsługuje warstwy, maski i zaawansowane narzędzia edycji.",
    "icon": "https://www.gimp.org/images/frontpage/wilber-big.png",
    "install_command": "sudo isolator install gimp",
    "remove_command": "sudo isolator remove gimp",
    "update_command": "sudo isolator update gimp",
    "check_command": "isolator list | grep gimp"
  },
  {
    "name": "VLC",
    "description": "Wszechstronny odtwarzacz multimedialny obsługujący wiele formatów audio i video bez dodatkowych kodeków.",
    "icon": "https://www.videolan.org/images/logo.png",
    "install_command": "sudo isolator install vlc",
    "remove_command": "sudo isolator remove vlc",
    "update_command": "sudo isolator update vlc",
    "check_command": "isolator list | grep vlc"
  },
  {
    "name": "Firefox",
    "description": "Szybka i prywatna przeglądarka internetowa z zaawansowanymi funkcjami ochrony prywatności.",
    "icon": "https://www.mozilla.org/media/protocol/img/logos/firefox/browser/logo.eb1324e44442.svg",
    "install_command": "sudo isolator install firefox",
    "remove_command": "sudo isolator remove firefox",
    "update_command": "sudo isolator update firefox",
    "check_command": "isolator list | grep firefox"
  },
  {
    "name": "LibreOffice",
    "description": "Kompletny pakiet biurowy zawierający edytor tekstu, arkusze kalkulacyjne, prezentacje i wiele więcej.",
    "icon": "https://www.libreoffice.org/assets/Uploads/LibreOffice-Initial-Artwork-Icons/LibreOffice-Initial-Artwork-Icons-64px.png",
    "install_command": "sudo isolator install libreoffice",
    "remove_command": "sudo isolator remove libreoffice",
    "update_command": "sudo isolator update libreoffice",
    "check_command": "isolator list | grep libreoffice"
  },
  {
    "name": "Krita",
    "description": "Zaawansowany edytor graficzny dla artystów cyfrowych, świetny do malarstwa i ilustracji.",
    "icon": "https://krita.org/wp-content/uploads/2022/02/krita_logo_300x300.png",
    "install_command": "sudo isolator install krita",
    "remove_command": "sudo isolator remove krita",
    "update_command": "sudo isolator update krita",
    "check_command": "isolator list | grep krita"
  },
  {
    "name": "OBS Studio",
    "description": "Oprogramowanie do nagrywania ekranu i streamingu na żywo.",
    "icon": "https://obsproject.com/assets/images/new_icon_small-r.png",
    "install_command": "sudo isolator install obs-studio",
    "remove_command": "sudo isolator remove obs-studio",
    "update_command": "sudo isolator update obs-studio",
    "check_command": "isolator list | grep obs-studio"
  },
  {
    "name": "Steam",
    "description": "Platforma do gier i zarządzania biblioteką gier komputerowych.",
    "icon": "https://store.cloudflare.steamstatic.com/public/shared/images/header/logo_steam.svg",
    "install_command": "sudo isolator install steam",
    "remove_command": "sudo isolator remove steam",
    "update_command": "sudo isolator update steam",
    "check_command": "isolator list | grep steam"
  },
  {
    "name": "Discord",
    "description": "Aplikacja do komunikacji głosowej, wideo i czatów tekstowych dla graczy i społeczności.",
    "icon": "https://cdn.worldvectorlogo.com/logos/discord-6.svg",
    "install_command": "sudo isolator install discord",
    "remove_command": "sudo isolator remove discord",
    "update_command": "sudo isolator update discord",
    "check_command": "isolator list | grep discord"
  },
  {
    "name": "Chromium",
    "description": "Otwartoźródłowa wersja przeglądarki Google Chrome.",
    "icon": "https://upload.wikimedia.org/wikipedia/commons/8/87/Chromium_Logo.svg",
    "install_command": "sudo isolator install chromium",
    "remove_command": "sudo isolator remove chromium",
    "update_command": "sudo isolator update chromium",
    "check_command": "isolator list | grep chromium"
  },
  {
    "name": "Kdenlive",
    "description": "Profesjonalny edytor wideo typu open-source z obsługą wielu formatów i efektów.",
    "icon": "https://kdenlive.org/wp-content/uploads/kdenlive-logo-300x300.png",
    "install_command": "sudo isolator install kdenlive",
    "remove_command": "sudo isolator remove kdenlive",
    "update_command": "sudo isolator update kdenlive",
    "check_command": "isolator list | grep kdenlive"
  },
  {
    "name": "Inkscape",
    "description": "Edytor grafiki wektorowej do tworzenia ilustracji i logotypów.",
    "icon": "https://media.inkscape.org/static/images/inkscape-logo.svg",
    "install_command": "sudo isolator install inkscape",
    "remove_command": "sudo isolator remove inkscape",
    "update_command": "sudo isolator update inkscape",
    "check_command": "isolator list | grep inkscape"
  },
  {
    "name": "Audacity",
    "description": "Popularny edytor audio z obsługą wielu efektów i nagrywania wielościeżkowego.",
    "icon": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Audacity_Logo.svg",
    "install_command": "sudo isolator install audacity",
    "remove_command": "sudo isolator remove audacity",
    "update_command": "sudo isolator update audacity",
    "check_command": "isolator list | grep audacity"
  },
  {
    "name": "Thunderbird",
    "description": "Klient pocztowy z obsługą wielu kont, kalendarza i wtyczek.",
    "icon": "https://www.thunderbird.net/media/img/thunderbird/thunderbird-256.png",
    "install_command": "sudo isolator install thunderbird",
    "remove_command": "sudo isolator remove thunderbird",
    "update_command": "sudo isolator update thunderbird",
    "check_command": "isolator list | grep thunderbird"
  },
  {
    "name": "VirtualBox",
    "description": "Oprogramowanie do wirtualizacji, umożliwiające uruchamianie wielu systemów operacyjnych.",
    "icon": "https://www.virtualbox.org/graphics/vbox_logo2_gradient.png",
    "install_command": "sudo isolator install virtualbox",
    "remove_command": "sudo isolator remove virtualbox",
    "update_command": "sudo isolator update virtualbox",
    "check_command": "isolator list | grep virtualbox"
  }
]
    except json.JSONDecodeError:
        print(f"Error: 'packages.json' contains invalid JSON. Loading default package list.")
        return []

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
        self.setGraphicsEffect(QGraphicsOpacityEffect(self)) # Dla animacji fade-in
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
        self.install_button.setIcon(QIcon.fromTheme("download")) # Ikona pobierania
        self.install_button.setObjectName("primaryButton")
        self.install_button.setEnabled(not self.is_installed)
        self.install_button.clicked.connect(self.install_package)
        button_layout.addWidget(self.install_button)
        self.remove_button = QPushButton("Usuń")
        self.remove_button.setIcon(QIcon.fromTheme("delete")) # Ikona usuwania
        self.remove_button.setObjectName("secondaryButton")
        self.remove_button.setEnabled(self.is_installed)
        self.remove_button.clicked.connect(self.remove_package)
        button_layout.addWidget(self.remove_button)
        self.update_button = QPushButton("Aktualizuj")
        self.update_button.setIcon(QIcon.fromTheme("view-refresh")) # Ikona aktualizacji
        self.update_button.setObjectName("secondaryButton")
        self.update_button.setEnabled(self.is_installed)
        self.update_button.clicked.connect(self.update_package)
        button_layout.addWidget(self.update_button)
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
            self.update_button.setEnabled(True)
            self.style().polish(self.status_label) # Odśwież styl
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
            self.update_button.setEnabled(False)
            self.remove_button.setText("Usuń")
            self.style().polish(self.status_label) # Odśwież styl
        except subprocess.CalledProcessError:
            self.parent().parent().parent().statusBar().showMessage("Błąd podczas usuwania!", 5000)
            self.remove_button.setEnabled(True)
            self.remove_button.setText("Usuń")

    def update_package(self):
        self.update_button.setEnabled(False)
        self.update_button.setText("Aktualizowanie...")
        QTimer.singleShot(100, lambda: self._update_package())

    def _update_package(self):
        try:
            subprocess.run(self.pkg["update_command"], shell=True, check=True)
            self.parent().parent().parent().statusBar().showMessage(f"{self.pkg['name']} zaktualizowany pomyślnie!", 5000)
            self.update_button.setEnabled(True)
            self.update_button.setText("Aktualizuj")
        except subprocess.CalledProcessError:
            self.parent().parent().parent().statusBar().showMessage("Błąd podczas aktualizacji!", 5000)
            self.update_button.setEnabled(True)
            self.update_button.setText("Aktualizuj")

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
    # Wbudowany styl QSS
    style_sheet = """
/* Zaawansowany styl Material Design (jeszcze ładniejszy, z gradientami i animacjami) */
/* Ogólne tło aplikacji */
QMainWindow {
    background-color: #F3F4F6; /* Lżejsze szare tło dla głębi */
}
/* App Bar */
QWidget#appBar {
    background-color: #2196F3; /* Material Blue */
    border-bottom: 1px solid #1976D2;
    color: white;
}
QLabel#appBarTitle {
    font-size: 20px;
    font-weight: bold;
    color: white;
}
QToolButton#appBarButton {
    background-color: transparent;
    border: none;
    color: white;
    font-size: 18px;
}
QToolButton#appBarButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
QToolButton#appBarButton:pressed {
    background-color: rgba(255, 255, 255, 0.2);
}
/* Pasek wyszukiwania */
QLineEdit#searchBar {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 28px; /* Bardziej zaokrąglone */
    padding: 12px 20px;
    font-size: 16px;
    color: #212121;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
QLineEdit#searchBar:focus {
    border: 2px solid #2196F3;
    box-shadow: 0 2px 6px rgba(33, 150, 243, 0.3);
}
/* Karta paczki */
QWidget#packageCard {
    background-color: #FFFFFF;
    border-radius: 16px; /* Większe zaokrąglenie */
    margin: 8px 0;
    padding: 0px;
    border: 1px solid #E8EAF6;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* Głębszy cień */
    transition: box-shadow 0.3s ease;
}
QWidget#packageCard:hover {
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12); /* Efekt podniesienia na hover */
    background-color: #FAFAFA;
}
/* Nazwa paczki */
QLabel#packageName {
    color: #212121;
    font-size: 18px;
    font-weight: 600;
}
/* Opis paczki */
QLabel#packageDesc {
    color: #616161;
    font-size: 14px;
}
/* Etykieta statusu */
QLabel#statusLabel {
    color: #4CAF50; /* Zielony dla zainstalowanego */
    font-size: 12px;
    font-weight: bold;
    background-color: #E8F5E9;
    border-radius: 4px;
    padding: 4px 8px;
}
QLabel#statusLabelNotInstalled {
    color: #F44336; /* Czerwony dla nie zainstalowanego */
    font-size: 12px;
    font-weight: bold;
    background-color: #FFEBEE;
    border-radius: 4px;
    padding: 4px 8px;
}
/* Przyciski */
QPushButton#primaryButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2196F3, stop:1 #1976D2); /* Gradient dla głębi */
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    box-shadow: 0 2px 4px rgba(33, 150, 243, 0.3);
    transition: box-shadow 0.2s ease;
}
QPushButton#primaryButton:hover {
    box-shadow: 0 4px 8px rgba(33, 150, 243, 0.4);
}
QPushButton#primaryButton:pressed {
    background-color: #1565C0;
    box-shadow: 0 1px 2px rgba(33, 150, 243, 0.2);
}
QPushButton#primaryButton:disabled {
    background-color: #B0BEC5;
    color: #78909C;
    box-shadow: none;
}
QPushButton#secondaryButton {
    background-color: transparent;
    color: #2196F3;
    border: 2px solid #2196F3;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    transition: background-color 0.2s ease;
}
QPushButton#secondaryButton:hover {
    background-color: rgba(33, 150, 243, 0.08);
}
QPushButton#secondaryButton:pressed {
    background-color: rgba(33, 150, 243, 0.16);
}
QPushButton#secondaryButton:disabled {
    border-color: #B0BEC5;
    color: #B0BEC5;
}
/* Floating Action Button (FAB) */
QPushButton#fab {
    background-color: #FF4081; /* Material Pink Accent */
    color: white;
    border: none;
    border-radius: 28px;
    font-size: 24px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
}
QPushButton#fab:hover {
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    transform: scale(1.1);
}
QPushButton#fab:pressed {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    transform: scale(0.95);
}
/* Pasek przewijania */
QScrollArea {
    border: none;
    background-color: transparent;
}
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #B0BEC5;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
/* Pasek postępu (ładowanie ikon) */
QProgressBar#iconProgress {
    border: none;
    background: transparent;
    border-radius: 32px;
}
QProgressBar#iconProgress::chunk {
    background-color: #2196F3;
    border-radius: 32px;
}
/* Status bar (Snackbar-like) */
QStatusBar#snackBar {
    background-color: #323232;
    color: white;
    font-size: 14px;
    padding: 8px 16px;
    border-top: 1px solid #424242;
}
/* Wiadomości dialogowe (zapasowe) */
QMessageBox {
    background-color: #FFFFFF;
    color: #212121;
}
QMessageBox QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
}
QMessageBox QPushButton:hover {
    background-color: #1976D2;
}
    """
    app.setStyleSheet(style_sheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
