# QGISExportToPDF

Export QGIS print layouts to PDF without a GUI. Designed to run as a scheduled server-side script. Used to generate maps for [firealertmap.com](https://firealertmap.com) ([source](https://github.com/luckydsf/firealertmap)).

Both **Windows** and **Ubuntu** versions are included.

---

## Prerequisites

### Windows

- [OSGeo4W](https://trac.osgeo.org/osgeo4w/) with **QGIS LTR** installed (installs to `C:\OSGeo4W` by default)
- Python available via the OSGeo4W shell (`python-qgis-ltr`)
- [pypdf](https://pypi.org/project/pypdf/) — install inside the OSGeo4W shell:
  ```
  pip install pypdf
  ```

### Ubuntu

- QGIS installed via the standard package manager (`qgis`, `python3-qgis`)
- [PyPDF2](https://pypi.org/project/PyPDF2/):
  ```
  pip install PyPDF2
  ```

---

## Configuration

Before running the script, update the path variables near the top of `nogui.py` to match your environment.

### Windows (`nogui.py`)

```python
QGIS_PATH = r"C:\OSGeo4W\apps\qgis-ltr"          # Path to your QGIS LTR install
PYTHON_PLUGINS = r"C:\OSGeo4W\apps\qgis-ltr\python\plugins"

qgz_path = r'C:\path\to\your\exportToPDF'         # Folder containing FireMap.qgz
pdf_path = qgz_path                                # Where PDFs are written (same folder by default)
web_path = r'C:\path\to\your\website\public\pdf'  # Where PDFs are copied for the web server
```

### Ubuntu (`ubuntu/ExportToPDF/nogui.py`)

```python
qgz_path = '/usr/share/pyshared/exportToPDF'   # Folder containing FireMap.qgz
pdf_path = qgz_path
web_path = '/var/www/firealertmap/pdf'          # Web server PDF folder
prefix_path = '/usr'                            # QGIS prefix path
plugins = '/usr/share/qgis/python/plugins'      # QGIS plugins folder
```

---

## Usage

### Windows

Run from the **OSGeo4W Shell**:

```
python-qgis-ltr nogui.py
```

### Ubuntu

```
python3 nogui.py
```

The script will:

1. Load `FireMap.qgz`
2. Export each print layout (`Northern_California`, `Sacramento`, `Central_Valley`) to its own PDF
3. Merge all section PDFs into `Fire_Severity_Maps.pdf`
4. Copy all PDFs to the configured `web_path`

---

## Project Structure

```
exportToPDF/
├── nogui.py              # Windows version
├── FireMap.qgz           # QGIS project file
├── shapefiles/           # Shapefiles used by the QGIS project
├── ubuntu/
│   └── ExportToPDF/
│       ├── nogui.py      # Ubuntu/Linux version
│       └── shapefiles/
└── SECURITY.md
```

---

## License

[GPL-2.0](LICENSE)
