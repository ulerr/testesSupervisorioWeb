fn main() {
    // Set encoding environment variables during build for consistent behavior
    std::env::set_var("PYTHONIOENCODING", "utf-8");
    std::env::set_var("PYTHONUTF8", "1");
    
    // Ensure UTF-8 locale is used during build
    if std::env::var("LC_ALL").is_err() {
        std::env::set_var("LC_ALL", "C.UTF-8");
    }
    if std::env::var("LANG").is_err() {
        std::env::set_var("LANG", "C.UTF-8");
    }
    
    tauri_build::build()
}
