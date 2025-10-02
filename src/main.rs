use eframe::{App, NativeOptions};
use package_manager::app::PackageManagerApp;

fn main() {
    let options = NativeOptions::default();
    eframe::run_native(
        "Menedżer Paczek",
        options,
        Box::new(|cc| Box::new(PackageManagerApp::new(cc))),
    );
}
