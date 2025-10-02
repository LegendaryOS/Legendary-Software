use egui::{Align2, CentralPanel, Context, Image, ScrollArea, Ui, Vec2, Window};
use std::sync::{Arc, Mutex};
use std::thread;

use eframe::epaint::TextureId;
use eframe::{CreationContext, Frame};

use crate::package::Package;
use crate::utils::{is_package_installed, load_packages};

pub struct PackageManagerApp {
    packages: Vec<Package>,
    filtered_packages: Vec<Package>,
    search_text: String,
    status_message: String,
    icons: Arc<Mutex<Vec<Option<egui::TextureHandle>>>>, // Cache for icons
}

impl PackageManagerApp {
    pub fn new(cc: &CreationContext<'_>) -> Self {
        let packages = load_packages();
        let filtered_packages = packages.clone();
        let icons = Arc::new(Mutex::new(vec![None; packages.len()]));

        // Load icons in background
        let icons_clone = icons.clone();
        let packages_clone = packages.clone();
        let egui_ctx = cc.egui_ctx.clone();
        thread::spawn(move || {
            for (i, pkg) in packages_clone.iter().enumerate() {
                if let Ok(response) = reqwest::blocking::get(&pkg.icon) {
                    if let Ok(data) = response.bytes() {
                        if let Ok(img) = image::load_from_memory(&data) {
                            let rgba = img.to_rgba8();
                            let size = [rgba.width() as usize, rgba.height() as usize];
                            let pixels = rgba.into_vec();
                            let texture = egui_ctx.load_texture(
                                &pkg.name,
                                egui::ColorImage::from_rgba_unmultiplied(size, &pixels),
                                egui::TextureOptions::default(),
                            );
                            icons_clone.lock().unwrap()[i] = Some(texture);
                        }
                    }
                }
                egui_ctx.request_repaint();
            }
        });

        Self {
            packages,
            filtered_packages,
            search_text: String::new(),
            status_message: String::new(),
            icons,
        }
    }

    fn show_status(&mut self, ui: &mut Ui) {
        if !self.status_message.is_empty() {
            ui.label(&self.status_message);
            // Clear after some time
            // In immediate mode, we can use a timer, but for simplicity, clear on next frame
        }
    }
}

impl eframe::App for PackageManagerApp {
    fn update(&mut self, ctx: &Context, _frame: &mut Frame) {
        CentralPanel::default().show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.label("Szukaj paczek:");
                ui.text_edit_singleline(&mut self.search_text);
                if ui.button("Odśwież").clicked() {
                    self.packages = load_packages();
                    self.filter_packages();
                    self.status_message = "Lista odświeżona".to_string();
                }
            });

            self.show_status(ui);

            ScrollArea::vertical().show(ui, |ui| {
                for (i, pkg) in self.filtered_packages.iter().enumerate() {
                    ui.horizontal(|ui| {
                        // Icon
                        if let Some(texture) = &self.icons.lock().unwrap()[i] {
                            let texture_id: TextureId = texture.id();
                            ui.add(Image::new(texture_id, Vec2::new(64.0, 64.0)));
                        } else {
                            ui.label("Ładowanie ikony...");
                        }

                        ui.vertical(|ui| {
                            ui.label(&pkg.name);
                            ui.label(&pkg.description);
                            let installed = is_package_installed(&pkg.check_command);
                            ui.label(if installed { "Zainstalowane" } else { "Nie zainstalowane" });

                            if ui.button("Zainstaluj").clicked() && !installed {
                                if let Ok(_) = std::process::Command::new("sh")
                                    .arg("-c")
                                    .arg(&pkg.install_command)
                                    .output() {
                                    self.status_message = format!("{} zainstalowany pomyślnie!", pkg.name);
                                } else {
                                    self.status_message = "Błąd podczas instalacji!".to_string();
                                }
                            }

                            if ui.button("Remove").clicked() && installed {
                                if let Ok(_) = std::process::Command::new("sh")
                                    .arg("-c")
                                    .arg(&pkg.remove_command)
                                    .output() {
                                    self.status_message = format!("{} usunięty pomyślnie!", pkg.name);
                                } else {
                                    self.status_message = "Błąd podczas usuwania!".to_string();
                                }
                            }

                            if ui.button("Aktualizuj").clicked() && installed {
                                if let Ok(_) = std::process::Command::new("sh")
                                    .arg("-c")
                                    .arg(&pkg.update_command)
                                    .output() {
                                    self.status_message = format!("{} zaktualizowany pomyślnie!", pkg.name);
                                } else {
                                    self.status_message = "Błąd podczas aktualizacji!".to_string();
                                }
                            }
                        });
                    });
                    ui.separator();
                }
            });

            // FAB simulation
            Window::new("FAB")
                .anchor(Align2::RIGHT_BOTTOM, [-16.0, -16.0])
                .title_bar(false)
                .resizable(false)
                .show(ctx, |ui| {
                    if ui.button("+").clicked() {
                        self.status_message = "Dodawanie nowej paczki (funkcja w rozwoju)".to_string();
                    }
                });
        });

        if !self.search_text.is_empty() {
            self.filter_packages();
        } else {
            self.filtered_packages = self.packages.clone();
        }
    }
}

impl PackageManagerApp {
    fn filter_packages(&mut self) {
        self.filtered_packages = self
            .packages
            .iter()
            .filter(|pkg| {
                pkg.name.to_lowercase().contains(&self.search_text.to_lowercase())
                    || pkg.description.to_lowercase().contains(&self.search_text.to_lowercase())
            })
            .cloned()
            .collect();
    }
}
