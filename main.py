import flet as ft
import json
import subprocess
import os

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

# Główna funkcja aplikacji
def main(page: ft.Page):
    page.title = "Menedżer Paczek"
    page.window.width = 600
    page.window.height = 400
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Funkcja do instalacji paczki
    def install_package(e, install_command, button, remove_button):
        try:
            subprocess.run(install_command, shell=True, check=True)
            page.snack_bar = ft.SnackBar(ft.Text("Paczka zainstalowana pomyślnie!"))
            page.snack_bar.open = True
            button.disabled = True
            remove_button.disabled = False
            page.update()
        except subprocess.CalledProcessError:
            page.snack_bar = ft.SnackBar(ft.Text("Błąd podczas instalacji!"))
            page.snack_bar.open = True
            page.update()

    # Funkcja do usuwania paczki
    def remove_package(e, remove_command, button, install_button):
        try:
            subprocess.run(remove_command, shell=True, check=True)
            page.snack_bar = ft.SnackBar(ft.Text("Paczka usunięta pomyślnie!"))
            page.snack_bar.open = True
            button.disabled = True
            install_button.disabled = False
            page.update()
        except subprocess.CalledProcessError:
            page.snack_bar = ft.SnackBar(ft.Text("Błąd podczas usuwania!"))
            page.snack_bar.open = True
            page.update()

    # Wczytanie paczek
    packages = load_packages()

    # Lista paczek w GUI
    package_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    for pkg in packages:
        is_installed = is_package_installed(pkg["check_command"])
        
        # Przyciski
        install_button = ft.ElevatedButton(
            text="Zainstaluj",
            disabled=is_installed,
            on_click=lambda e, cmd=pkg["install_command"], btn=install_button, rm_btn=remove_button: install_package(e, cmd, btn, rm_btn)
        )
        remove_button = ft.ElevatedButton(
            text="Usuń",
            disabled=not is_installed,
            on_click=lambda e, cmd=pkg["remove_command"], btn=remove_button, inst_btn=install_button: remove_package(e, cmd, btn, inst_btn)
        )

        # Wiersz z paczką
        package_row = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src=pkg["icon"], width=50, height=50, fit=ft.ImageFit.CONTAIN),
                    ft.Column(
                        [
                            ft.Text(pkg["name"], weight=ft.FontWeight.BOLD),
                            ft.Text(pkg["description"], width=300)
                        ]
                    ),
                    install_button,
                    remove_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            margin=5
        )
        package_list.controls.append(package_row)

    # Dodanie listy do strony
    page.add(
        ft.Text("Menedżer Paczek", size=24, weight=ft.FontWeight.BOLD),
        package_list
    )

# Uruchomienie aplikacji
ft.app(target=main)
