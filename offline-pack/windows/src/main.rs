use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn write(path: PathBuf, bytes: &[u8]) {
    if let Some(parent) = path.parent() {
        let _ = fs::create_dir_all(parent);
    }
    let _ = fs::write(path, bytes);
}

fn main() {
    let base = env::var("LOCALAPPDATA").unwrap_or_else(|_| env::temp_dir().display().to_string());
    let dir = PathBuf::from(base).join("RabeyaClass5English");
    write(
        dir.join("index.html"),
        include_bytes!("../../../offline-pack/web/index.html"),
    );
    write(
        dir.join("exam.html"),
        include_bytes!("../../../offline-pack/web/exam.html"),
    );
    write(
        dir.join("favicon.svg"),
        include_bytes!("../../../offline-pack/web/favicon.svg"),
    );
    write(
        dir.join("preview/page-1.png"),
        include_bytes!("../../../offline-pack/web/preview/page-1.png"),
    );
    write(
        dir.join("preview/page-2.png"),
        include_bytes!("../../../offline-pack/web/preview/page-2.png"),
    );
    write(
        dir.join("downloads/Rabeya_Coaching_Center_Class5_English_SMT04.docx"),
        include_bytes!("../../../offline-pack/web/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.docx"),
    );
    write(
        dir.join("downloads/Rabeya_Coaching_Center_Class5_English_SMT04.pdf"),
        include_bytes!("../../../offline-pack/web/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.pdf"),
    );
    write(
        dir.join("downloads/class5-english-source.pdf"),
        include_bytes!("../../../offline-pack/web/downloads/class5-english-source.pdf"),
    );
    let index = dir.join("index.html");
    let _ = Command::new("cmd")
        .args(["/C", "start", "", &index.to_string_lossy()])
        .spawn();
}
