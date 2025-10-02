use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Package {
    pub name: String,
    pub description: String,
    pub icon: String,
    pub install_command: String,
    pub remove_command: String,
    pub update_command: String,
    pub check_command: String,
}
