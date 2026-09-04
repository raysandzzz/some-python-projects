import datetime
import json
import os
import tkinter as tk
import ctypes

THEMES = {
    "dark": {
        "bg": "#181824",
        "sidebar": "#12121b",
        "card": "#222334",
        "text": "#cdd6f4",
        "accent": "#a6e3a1",
        "muted": "#6c7086",
        "btn_active": "#2f314c",
        "danger": "#f38ba8",
    }
}

class SimpleChecklistApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simple Checklist")
        self.root.geometry("640x500")
        self.root.resizable(False, False)

        # Typography state and dynamic scale definitions
        self.use_pixel_font = False
        self._update_font_definitions()

        # Visual theme configuration
        self.theme = THEMES["dark"]
        self.root.configure(bg=self.theme["bg"])

        # Determine path to the local JSON database
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(self.base_dir, "tasks.json")

        # Load stored records and verify daily reset
        self.data = self._load_data()
        self._check_midnight_reset()

        # Track active view for screen transitions and font refreshes
        self.current_screen = None
        self.current_screen_type = "daily"

        # Build interface layout and display default view
        self._build_layout()
        self.show_daily_screen()

    # =========================================================================
    # Typography Setup & Dynamic Switcher
    # =========================================================================
    def _update_font_definitions(self):
        """Updates internal font tuples to match the selected typography style."""
        if self.use_pixel_font:
            family = "Minecraft"
            self.f_sidebar_title = (family, 16)
            self.f_nav = (family, 10)
            self.f_title = (family, 24)
            self.f_subtitle = (family, 8)
            self.f_body = (family, 12)
            self.f_btn = (family, 10)
            self.f_footer = (family, 10)
        else:
            family = "Segoe UI"
            self.f_sidebar_title = (family, 14, "bold")
            self.f_nav = (family, 11, "bold")
            self.f_title = (family, 22, "bold")
            self.f_subtitle = (family, 10)
            self.f_body = (family, 11)
            self.f_btn = (family, 10, "bold")
            self.f_footer = (family, 10)

    def _toggle_font(self):
        """Toggles between pixel and standard font, refreshing all UI elements."""
        self.use_pixel_font = not self.use_pixel_font
        self._update_font_definitions()

        # Refresh static sidebar text styles
        self.lbl_sidebar_title.config(font=self.f_sidebar_title)
        self.btn_nav_daily.config(font=self.f_nav)
        self.btn_nav_general.config(font=self.f_nav)
        self.btn_toggle_font.config(
            text="Font: Pixel" if self.use_pixel_font else "Font: Clean",
            font=self.f_footer,
        )

        # Redraw the active screen
        if self.current_screen_type == "general":
            self.show_general_screen()
        else:
            self.show_daily_screen()

    # =========================================================================
    # Data Persistence and Midnight Reset
    # =========================================================================
    def _load_data(self) -> dict:
        """Loads tasks from local JSON storage or returns clean defaults."""
        today_str = datetime.date.today().isoformat()
        default_data = {
            "last_date": today_str,
            "daily_tasks": [],
            "general_tasks": [],
        }

        if not os.path.exists(self.data_file):
            return default_data

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_data

    def _save_data(self):
        """Writes current task lists to disk."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def _check_midnight_reset(self):
        """Unchecks daily habits when the recorded date does not match today."""
        today_str = datetime.date.today().isoformat()
        if self.data.get("last_date") != today_str:
            for task in self.data["daily_tasks"]:
                task["done"] = False
            self.data["last_date"] = today_str
            self._save_data()

    # =========================================================================
    # Main Structure (Sidebar & Container)
    # =========================================================================
    def _build_layout(self):
        """Constructs the sidebar navigation and dynamic content workspace."""
        # Fixed left sidebar
        self.sidebar = tk.Frame(
            self.root, bg=self.theme["sidebar"], width=160, padx=14, pady=20
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Discrete font toggle button at the bottom-left
        self.btn_toggle_font = tk.Button(
            self.sidebar,
            text="Font: Clean",
            font=self.f_footer,
            bg=self.theme["sidebar"],
            fg=self.theme["muted"],
            activebackground=self.theme["sidebar"],
            activeforeground=self.theme["accent"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor="w",
            command=self._toggle_font,
        )
        self.btn_toggle_font.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Brand header
        self.lbl_sidebar_title = tk.Label(
            self.sidebar,
            text="CHECKLIST",
            font=self.f_sidebar_title,
            bg=self.theme["sidebar"],
            fg=self.theme["accent"],
        )
        self.lbl_sidebar_title.pack(anchor="w", pady=(0, 25))

        # Navigation buttons
        self.btn_nav_daily = tk.Button(
            self.sidebar,
            text="  Daily Tasks",
            font=self.f_nav,
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["accent"],
            relief=tk.FLAT,
            anchor="w",
            cursor="hand2",
            pady=6,
            command=self.show_daily_screen,
        )
        self.btn_nav_daily.pack(fill=tk.X, pady=4)

        self.btn_nav_general = tk.Button(
            self.sidebar,
            text="  General",
            font=self.f_nav,
            bg=self.theme["sidebar"],
            fg=self.theme["muted"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["text"],
            relief=tk.FLAT,
            anchor="w",
            cursor="hand2",
            pady=6,
            command=self.show_general_screen,
        )
        self.btn_nav_general.pack(fill=tk.X, pady=4)

        # Dynamic screen container
        self.main_container = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_container.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=25, pady=20
        )

    def _switch_screen(self, new_screen: tk.Frame):
        """Removes the prior screen frame and mounts the newly selected one."""
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = new_screen
        self.current_screen.pack(fill=tk.BOTH, expand=True)

    # =========================================================================
    # View 1: Daily Tasks
    # =========================================================================
    def show_daily_screen(self):
        """Displays recurring daily habits with date header."""
        self.current_screen_type = "daily"
        self.btn_nav_daily.config(
            fg=self.theme["accent"], bg=self.theme["card"]
        )
        self.btn_nav_general.config(
            fg=self.theme["muted"], bg=self.theme["sidebar"]
        )

        screen = tk.Frame(self.main_container, bg=self.theme["bg"])

        now = datetime.datetime.now()
        day_str = now.strftime("%A").upper()
        date_str = now.strftime("%B %d, %Y")

        header_frame = tk.Frame(screen, bg=self.theme["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 15))

        lbl_day = tk.Label(
            header_frame,
            text=day_str,
            font=self.f_title,
            bg=self.theme["bg"],
            fg=self.theme["accent"],
        )
        lbl_day.pack(anchor="w")

        lbl_date = tk.Label(
            header_frame,
            text=date_str,
            font=self.f_subtitle,
            bg=self.theme["bg"],
            fg=self.theme["muted"],
        )
        lbl_date.pack(anchor="w")

        # Input row
        entry_frame = tk.Frame(screen, bg=self.theme["bg"])
        entry_frame.pack(fill=tk.X, pady=(5, 15))

        self.daily_entry = tk.Entry(
            entry_frame,
            font=self.f_body,
            bg=self.theme["card"],
            fg=self.theme["text"],
            insertbackground=self.theme["accent"],
            relief=tk.FLAT,
        )
        self.daily_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.daily_entry.bind("<Return>", lambda event: self._add_daily_task())

        btn_add = tk.Button(
            entry_frame,
            text="Add Habit",
            font=self.f_btn,
            bg=self.theme["accent"],
            fg=self.theme["sidebar"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["text"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._add_daily_task,
        )
        btn_add.pack(side=tk.RIGHT, padx=(8, 0))

        # Habit list area
        self.daily_list_frame = tk.Frame(screen, bg=self.theme["bg"])
        self.daily_list_frame.pack(fill=tk.BOTH, expand=True)

        self._render_daily_tasks()
        self._switch_screen(screen)

    def _render_daily_tasks(self):
        """Populates the daily habit rows."""
        for widget in self.daily_list_frame.winfo_children():
            widget.destroy()

        if not self.data["daily_tasks"]:
            empty_lbl = tk.Label(
                self.daily_list_frame,
                text="No daily habits registered yet.\nAdd one above to track it every day.",
                font=self.f_subtitle,
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                pady=30,
            )
            empty_lbl.pack()
            return

        for idx, task in enumerate(self.data["daily_tasks"]):
            row = tk.Frame(self.daily_list_frame, bg=self.theme["card"], pady=6)
            row.pack(fill=tk.X, pady=4)

            status_symbol = "✓" if task["done"] else "○"
            status_fg = (
                self.theme["accent"] if task["done"] else self.theme["muted"]
            )

            btn_toggle = tk.Button(
                row,
                text=status_symbol,
                font=self.f_nav,
                width=3,
                bg=self.theme["card"],
                fg=status_fg,
                activebackground=self.theme["card"],
                activeforeground=self.theme["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda i=idx: self._toggle_daily_task(i),
            )
            btn_toggle.pack(side=tk.LEFT, padx=(6, 8))

            text_fg = (
                self.theme["muted"] if task["done"] else self.theme["text"]
            )
            lbl_text = tk.Label(
                row,
                text=task["text"],
                font=self.f_body,
                bg=self.theme["card"],
                fg=text_fg,
                anchor="w",
            )
            lbl_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

            btn_del = tk.Button(
                row,
                text="✕",
                font=self.f_btn,
                bg=self.theme["card"],
                fg=self.theme["danger"],
                activebackground=self.theme["card"],
                activeforeground=self.theme["danger"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda i=idx: self._delete_daily_task(i),
            )
            btn_del.pack(side=tk.RIGHT, padx=8)

    def _add_daily_task(self):
        text = self.daily_entry.get().strip()
        if text:
            self.data["daily_tasks"].append({"text": text, "done": False})
            self._save_data()
            self.daily_entry.delete(0, tk.END)
            self._render_daily_tasks()

    def _toggle_daily_task(self, index: int):
        self.data["daily_tasks"][index]["done"] = not self.data["daily_tasks"][
            index
        ]["done"]
        self._save_data()
        self._render_daily_tasks()

    def _delete_daily_task(self, index: int):
        self.data["daily_tasks"].pop(index)
        self._save_data()
        self._render_daily_tasks()

    # =========================================================================
    # View 2: General Tasks Backlog
    # =========================================================================
    def show_general_screen(self):
        """Displays the persistent general backlog."""
        self.current_screen_type = "general"
        self.btn_nav_general.config(
            fg=self.theme["accent"], bg=self.theme["card"]
        )
        self.btn_nav_daily.config(
            fg=self.theme["muted"], bg=self.theme["sidebar"]
        )

        screen = tk.Frame(self.main_container, bg=self.theme["bg"])

        header_frame = tk.Frame(screen, bg=self.theme["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 15))

        lbl_title = tk.Label(
            header_frame,
            text="GENERAL BACKLOG",
            font=self.f_title,
            bg=self.theme["bg"],
            fg=self.theme["text"],
        )
        lbl_title.pack(anchor="w")

        lbl_desc = tk.Label(
            header_frame,
            text="Persistent to-do list for pending goals and projects.",
            font=self.f_subtitle,
            bg=self.theme["bg"],
            fg=self.theme["muted"],
        )
        lbl_desc.pack(anchor="w")

        # Input row
        entry_frame = tk.Frame(screen, bg=self.theme["bg"])
        entry_frame.pack(fill=tk.X, pady=(5, 15))

        self.general_entry = tk.Entry(
            entry_frame,
            font=self.f_body,
            bg=self.theme["card"],
            fg=self.theme["text"],
            insertbackground=self.theme["accent"],
            relief=tk.FLAT,
        )
        self.general_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.general_entry.bind(
            "<Return>", lambda event: self._add_general_task()
        )

        btn_add = tk.Button(
            entry_frame,
            text="Add Task",
            font=self.f_btn,
            bg=self.theme["accent"],
            fg=self.theme["sidebar"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["text"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._add_general_task,
        )
        btn_add.pack(side=tk.RIGHT, padx=(8, 0))

        # General list area
        self.general_list_frame = tk.Frame(screen, bg=self.theme["bg"])
        self.general_list_frame.pack(fill=tk.BOTH, expand=True)

        self._render_general_tasks()
        self._switch_screen(screen)

    def _render_general_tasks(self):
        """Populates general task rows."""
        for widget in self.general_list_frame.winfo_children():
            widget.destroy()

        if not self.data["general_tasks"]:
            empty_lbl = tk.Label(
                self.general_list_frame,
                text="No general tasks right now.\nAdd any pending items above.",
                font=self.f_subtitle,
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                pady=30,
            )
            empty_lbl.pack()
            return

        for idx, task in enumerate(self.data["general_tasks"]):
            row = tk.Frame(
                self.general_list_frame, bg=self.theme["card"], pady=6
            )
            row.pack(fill=tk.X, pady=4)

            status_symbol = "✓" if task["done"] else "○"
            status_fg = (
                self.theme["accent"] if task["done"] else self.theme["muted"]
            )

            btn_toggle = tk.Button(
                row,
                text=status_symbol,
                font=self.f_nav,
                width=3,
                bg=self.theme["card"],
                fg=status_fg,
                activebackground=self.theme["card"],
                activeforeground=self.theme["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda i=idx: self._toggle_general_task(i),
            )
            btn_toggle.pack(side=tk.LEFT, padx=(6, 8))

            text_fg = (
                self.theme["muted"] if task["done"] else self.theme["text"]
            )
            lbl_text = tk.Label(
                row,
                text=task["text"],
                font=self.f_body,
                bg=self.theme["card"],
                fg=text_fg,
                anchor="w",
            )
            lbl_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

            btn_del = tk.Button(
                row,
                text="✕",
                font=self.f_btn,
                bg=self.theme["card"],
                fg=self.theme["danger"],
                activebackground=self.theme["card"],
                activeforeground=self.theme["danger"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda i=idx: self._delete_general_task(i),
            )
            btn_del.pack(side=tk.RIGHT, padx=8)

    def _add_general_task(self):
        text = self.general_entry.get().strip()
        if text:
            self.data["general_tasks"].append({"text": text, "done": False})
            self._save_data()
            self.general_entry.delete(0, tk.END)
            self._render_general_tasks()

    def _toggle_general_task(self, index: int):
        self.data["general_tasks"][index]["done"] = not self.data[
            "general_tasks"
        ][index]["done"]
        self._save_data()
        self._render_general_tasks()

    def _delete_general_task(self, index: int):
        self.data["general_tasks"].pop(index)
        self._save_data()
        self._render_general_tasks()


def main():
    # Fix high DPI blurriness on Windows
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    root = tk.Tk()
    SimpleChecklistApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()