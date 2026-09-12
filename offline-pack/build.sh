#!/bin/bash
set -euo pipefail
ROOT=/workspace
PACK="$ROOT/offline-pack"
WEB="$PACK/web"
OUT="$ROOT/releases"
PUB="$ROOT/public/downloads"
ART="$ROOT/artifacts"
TOOLS=/tmp/tools
APKSRC=/tmp/apkwork/class5

rm -rf "$WEB"
mkdir -p "$WEB/downloads" "$WEB/preview" "$OUT" "$PUB" "$ART"

cp "$PACK/index.html" "$WEB/index.html"
cp "$ROOT/public/exam.html" "$WEB/exam.html"
cp "$ROOT/public/favicon.svg" "$WEB/favicon.svg"
cp "$ROOT/public/preview/page-1.png" "$WEB/preview/page-1.png"
cp "$ROOT/public/preview/page-2.png" "$WEB/preview/page-2.png"
cp "$ROOT/public/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.docx" "$WEB/downloads/"
cp "$ROOT/public/downloads/Rabeya_Coaching_Center_Class5_English_SMT04.pdf" "$WEB/downloads/"
cp "$ROOT/attachments/class 5 english.pdf" "$WEB/downloads/class5-english-source.pdf"

echo "== web pack ready =="

# --- APK ---
rm -rf "$APKSRC"
java -jar "$TOOLS/apktool.jar" d -f "$TOOLS/prottoyon.apk" -o "$APKSRC" >/tmp/apk-decode.log
python3 - << 'PY'
import pathlib, shutil, re
src = pathlib.Path("/tmp/apkwork/class5")
web = pathlib.Path("/workspace/offline-pack/web")
# replace assets
assets = src / "assets"
shutil.rmtree(assets)
shutil.copytree(web, assets)
# strings
(src / "res/values/strings.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <string name="app_name">Class 5 English</string>\n</resources>\n',
    encoding="utf-8",
)
# manifest
man = (src / "AndroidManifest.xml").read_text(encoding="utf-8")
man = man.replace('package="bd.rabeya.prottoyon"', 'package="bd.rabeya.class5english"')
man = man.replace('android:label="রাবেয়া প্রত্যয়ন"', 'android:label="Class 5 English"')
(src / "AndroidManifest.xml").write_text(man, encoding="utf-8")
# apktool.yml
yml = (src / "apktool.yml").read_text(encoding="utf-8")
yml = yml.replace("apkFileName: prottoyon.apk", "apkFileName: Class5-English-SMT04.apk")
yml = yml.replace("versionCode: 8", "versionCode: 1")
yml = yml.replace("versionName: 1.7", "versionName: 1.0")
(src / "apktool.yml").write_text(yml, encoding="utf-8")
# rename smali package
old = src / "smali/bd/rabeya/prottoyon"
new = src / "smali/bd/rabeya/class5english"
new.parent.mkdir(parents=True, exist_ok=True)
if new.exists():
    shutil.rmtree(new)
shutil.move(str(old), str(new))
for p in new.glob("*.smali"):
    t = p.read_text(encoding="utf-8")
    t = t.replace("Lbd/rabeya/prottoyon/", "Lbd/rabeya/class5english/")
    p.write_text(t, encoding="utf-8")
print("apk sources patched")
PY

# launcher icon from og.jpg if ffmpeg exists
if command -v ffmpeg >/dev/null 2>&1; then
  ffmpeg -y -i "$ROOT/public/og.jpg" -vf "scale=192:192:force_original_aspect_ratio=increase,crop=192:192" \
    "$APKSRC/res/drawable/ic_launcher.png" >/tmp/icon.log 2>&1 || true
fi

java -jar "$TOOLS/apktool.jar" b "$APKSRC" -o /tmp/class5-unsigned.apk
java -jar "$TOOLS/uber-apk-signer.jar" --apks /tmp/class5-unsigned.apk --out /tmp/apk-signed --allowResign
SIGNED=$(ls /tmp/apk-signed/*.apk | head -1)
cp "$SIGNED" "$OUT/Class5-English-SMT04.apk"
cp "$SIGNED" "$PUB/Class5-English-SMT04.apk"
cp "$SIGNED" "$ART/Class5-English-SMT04.apk"
echo "== apk $(wc -c < "$OUT/Class5-English-SMT04.apk") bytes =="

# standalone html zip + copies
cp "$WEB/index.html" "$OUT/index.html"
cp "$WEB/exam.html" "$OUT/exam.html"
python3 - << 'PY'
import shutil, zipfile, os
from pathlib import Path
web = Path("/workspace/offline-pack/web")
out = Path("/workspace/releases/Class5-English-SMT04-offline.zip")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in web.rglob("*"):
        if p.is_file():
            z.write(p, p.relative_to(web))
print("zip", out, out.stat().st_size)
shutil.copy2(out, "/workspace/public/downloads/Class5-English-SMT04-offline.zip")
shutil.copy2(out, "/workspace/artifacts/Class5-English-SMT04-offline.zip")
PY

echo BUILD_WEB_OK
