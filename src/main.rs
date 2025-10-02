use eframe::NativeOptions;
use legendary_software::app::PackageManagerApp;

fn main() {
    let options = NativeOptions::default();
    // Ignore Result for simplicity; in production, consider proper error handling
    let _ = eframe::run_native(
        "Menedżer Paczek",
        options,
        Box::new(|cc| Box::new(PackageManagerApp::new(cc))),
    );
}
