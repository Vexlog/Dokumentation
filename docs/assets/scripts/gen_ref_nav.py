from pathlib import Path
import os

import mkdocs_gen_files

def get_file_size(path):
    """Konvertiere Dateigröße in lesbares Format."""
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_file_info(file_path):
    """Extrahiere Datei-Informationen."""
    ext = file_path.suffix.lower()
    size = get_file_size(file_path)
    return ext, size

def generate_preview_content(doc_name, doc_path, file_ext, file_size):
    """Generiere Preview-Content basierend auf Dateityp."""
    content = f"# {doc_name}\n\n"
    
    # Info-Box
    content += f"""!!! info "Datei-Informationen"
    - **Format:** {file_ext.upper() if file_ext else 'Unbekannt'}
    - **Größe:** {file_size}

"""
    
    # Preview basierend auf Dateitype
    if file_ext == '.pdf':
        stem = doc_path.stem
        # Absoluter Pfad zum selbst gehosteten Viewer
        # viewer.html akzeptiert den `file`-Parameter als absoluten Pfad
        content += f"""## 📄 PDF-Vorschau

<div style="
    width: 100%;
    height: 90vh;
    min-height: 600px;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 4px;
    overflow: hidden;
">
  <iframe
    id="pdf-iframe-{stem}"
    src=""
    style="width:100%; height:100%; border:none;"
    allowfullscreen
  ></iframe>
</div>

<script>
(function() {{
  const base     = (document.querySelector('meta[name="site-url"]')?.content ?? '/').replace(/\\/$/, '');
  const pdfPath  = base + '/assets/downloads/{doc_path.name}';
  const viewer   = base + '/assets/js/pdfjs/web/viewer.html';
  document.getElementById('pdf-iframe-{stem}').src = viewer + '?file=' + encodeURIComponent(pdfPath);
}})();
</script>

!!! note "Hinweis"
    Falls die Vorschau nicht lädt, Dokument bitte herunterladen.

"""
    
    elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        content += f"""## 🖼️ Bild-Vorschau

![{doc_name}](../assets/downloads/{doc_path.name})

"""
    
    elif file_ext in ['.docx', '.doc']:
        content += f"""## 📝 Word-Dokument

Dieses Dokument ist ein Word-Format-Datei. Eine direkte Vorschau im Browser ist nicht möglich.

!!! warning "Vorschau nicht verfügbar"
    Word-Dokumente können in der Web-Ansicht nicht angezeigt werden. Bitte laden Sie das Dokument herunter.

"""
    
    elif file_ext in ['.xlsx', '.xls']:
        content += f"""## 📊 Excel-Tabelle

Dieses Dokument ist eine Excel-Datei. Eine direkte Vorschau im Browser ist nicht möglich.

!!! warning "Vorschau nicht verfügbar"
    Excel-Dateien können in der Web-Ansicht nicht angezeigt werden. Bitte laden Sie das Dokument herunter.

"""
    
    elif file_ext == '.md':
        content += f"""## 📄 Markdown-Datei

!!! note "Info"
    Dies ist eine Markdown-Datei. Sie wird als Text-Format gespeichert.

"""
    
    elif file_ext == '.drawio':
        content += f"""## 🎨 Draw.io Diagramm

Draw.io-Dateien können in der Browser-Vorschau nicht angezeigt werden.

!!! warning "Vorschau nicht verfügbar"
    Um dieses Diagramm zu bearbeiten oder anzusehen, verwenden Sie [draw.io](https://draw.io) oder ein kompatibles Tool.

"""
    
    elif file_ext == '.txt':
        content += f"""## 📋 Text-Datei

Dies ist eine Textdatei.

"""
    
    else:
        content += f"""## 📦 Binärdatei

Dieser Dateityp wird nicht in der Vorschau unterstützt.

"""
    
    # Download-Section
    content += f"""---

## ⬇️ Download

<a href="/assets/downloads/{doc_path.name}" class="md-button md-button--primary" download>
  📥 {doc_path.name} herunterladen
</a>

"""
    
    return content

nav = mkdocs_gen_files.Nav()

documents_path = Path("docs/assets/downloads")
files_list = []

for path in sorted(documents_path.glob("*")):
    if not path.is_file():
        continue

    stem     = path.stem
    filename = path.name
    file_ext, file_size = get_file_info(path)

    # Pfade konsistent halten – analog zum Reference-Script:
    # full_doc_path  → wo mkdocs_gen_files die Datei ablegt
    # nav_path       → relativ zum SUMMARY-Ordner (dateien/)
    nav_path      = f"{stem}.md"                   # relativ zu dateien/
    full_doc_path = Path("dateien") / nav_path     # dateien/stem.md

    # Nav: nur ein flacher Eintrag, kein verschachtelter Tuple-Key
    nav[stem] = nav_path

    files_list.append((stem, nav_path, filename))

    preview_content = generate_preview_content(
        stem,
        path.relative_to("docs"),
        file_ext,
        file_size,
    )

    with mkdocs_gen_files.open(full_doc_path, "w") as f:
        f.write(preview_content)

    # set_edit_path braucht denselben Pfad wie open()
    mkdocs_gen_files.set_edit_path(full_doc_path, path)
    print(f"Generated: {full_doc_path}")

# Index-Seite  (dateien/index.md)
with mkdocs_gen_files.open(Path("dateien") / "index.md", "w") as f:
    f.write("# 📂 Dokumente & Downloads\n\n")
    f.write("Zentrale Verwaltung aller projektbezogenen Dokumente und Ressourcen.\n\n")
    for stem, nav_path, filename in files_list:
        f.write(f"- [{stem}]({stem}.md)\n")

# SUMMARY muss im selben Ordner liegen wie die generierten Seiten
# → dateien/SUMMARY.txt  (nicht dateien/SUMMARY.md!)
with mkdocs_gen_files.open("dateien/SUMMARY.txt", "w") as f:
    f.writelines(nav.build_literate_nav())

print(f"\nGenerated {len(files_list)} document pages.")