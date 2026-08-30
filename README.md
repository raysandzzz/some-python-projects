# Some Python Projects :)

A collection of simple Python utilities, automation scripts, and small GUI applications designed to be functional and easy to use. Each one was built in a day or less.

---

## 📋 Overview

| Project | Category | Tech / Libraries | Description |
|---|---|---|---|
| [`file_sorter.py`](#file-sorter) | Script / Automation | `pathlib`, `shutil`, `argparse` | Organizes directory files by category with collision handling and undo support. |

---

## 🛠️ Projects

### Scripts

#### <ins>File Sorter</ins>
A lightweight automation tool that organizes files in a directory into categorized folders based on their extensions. It prevents overwriting through collision resolution, generates a local history log, and allows rolling back changes.

* **Location:** `scripts/file_sorter.py`
* **Dependencies:** None (Standard Library only: Python 3.8+)

**Features:**
* Categorizes files into `Images`, `Documents`, `Audio`, `Video`, `Compressed`, `Installers`, and `Code`.
* Automatic collision handling (e.g., renames duplicates to `file(1).ext`).
* Rollback system to revert moves and remove empty folders.
* Interactive menu on double-click or CLI command support.

**Usage:**

You can simply place `file_sorter.py` inside the folder you want to organize and double-click it. 

If you prefer or find it more convenient, you can also run it directly from your terminal using these commands:

* **Organize the current folder:**
  ```bash
  python file_sorter.py
  
* **Organize a specific folder without moving the script:**

  ```bash
  python file_sorter.py "path/to/target/folder"
  ```

* **Undo the last organization:**

  ```bash
  python file_sorter.py --undo
  python file_sorter.py "path/to/target/folder" --undo
  ```

* **Delete the history log (Lock changes permanently):**

  ```bash
  python file_sorter.py --clear-history
  ```
