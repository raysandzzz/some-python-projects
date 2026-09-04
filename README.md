# Some Python Projects.

A mini collection of simple Python utilities, automation scripts, and small GUI applications designed to be functional and easy to use. Each one was built in a day or less.

---

## 📋 Overview

| Project | Category | Tech / Libraries | Description |
| :--- | :--- | :--- | :--- |
| `file_sorter.py` | Script / Automation | `pathlib`, `shutil`, `argparse` | Organizes directory files by category with collision handling and undo support. |
| `password_generator.py` | Script / Security | `secrets`, `string` | Generates cryptographically secure passwords with custom character rules. |
| `pomodoro_timer.py` | Script / Productivity | `time` | Interactive Pomodoro timer with real-time CLI progress bars and audio alerts. |
| `decision_roulette.py` | Script / Utility | `secrets`, `time` | A marquee-style animated decision roulette with realistic deceleration. |
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

#### <ins>Password Generator</ins>

Generates cryptographically secure random passwords. It features custom length and character set selection. 

* **Location:** `scripts/password_gen.py`
* **Dependencies:** None (Standard Library only: Python 3.8+)

**Features:**

* Cryptographically secure randomness powered by Python's `secrets` module.
* Guarantees at least one character of each selected type (uppercase, digits, symbols) to meet standard password policy requirements.
* Configurable password length and character sets.
* Support for generating single or multiple passwords in a single run.
* Interactive step-by-step CLI interface with strict input validation.

**Usage:**

You can simply double-click `password_gen.py` or run it directly from your terminal:

* **Run the interactive generator:**
  ```bash
  python password_gen.py

#### <ins>CLI Pomodoro Timer</ins>

A simple CLI timer to help you keep focused, with clean progress bars and work/break sessions.

* **Location:** `scripts/pomodoro_timer.py`
* **Dependencies:** None (Standard Library only: Python 3.8+)

**Features:**

* Real-time animated progress bar right in your terminal.
* Quick presets (25/5 min, 15/3 min) or custom study/break times.
* System sound alert when your time is up.
* Quick cancel anytime by pressing `Ctrl + C`.
* Easy defaults: just press Enter to start.

**Usage:**

You can simply double-click `pomodoro_timer.py` or run it directly from your terminal:

* **Run the interactive generator:**
  ```bash
  python pomodoro_timer.py

#### <ins>Decision Roulette</ins>

A simple CLI decision-maker that spins through your choices with fair random picks.

* **Location:** `scripts/decision_roulette.py`
* **Dependencies:** None (Standard Library only: Python 3.8+)

**Features:**

* Animated marquee frame that slows down naturally to pick a winner.
* Unbiased random selection powered by `secrets`.
* Custom options support

**Usage:**

Double-click `decision_wheel.py` or run:

```bash
python decision_wheel.py


---
### Tkinter apps