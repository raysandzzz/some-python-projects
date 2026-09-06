"""Simple Checklist application entry point and screen coordinator."""

import ctypes
import os
import tkinter as tk

from config import THEMES, get_font_definitions
from task_manager import TaskManager
from views import DailyView, GeneralView, Sidebar


class SimpleChecklistApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Checklist App")
        self.root.geometry("760x540")
        self.root.minsize(700, 480)
        self.root.resizable(False, False)
        
        # Set icon
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "check_icon.png")
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(
                file=icon_path
            )  # Guardar referencia en self
            self.root.iconphoto(True, self.icon)

        # Initialize core manager and configuration
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.task_manager = TaskManager(os.path.join(base_dir, "tasks.json"))

        self.theme = THEMES["dark"]
        self.root.configure(bg=self.theme["bg"])
        self.fonts = get_font_definitions(self.task_manager.use_pixel_font)

        # State trackers
        self.current_screen = None
        self.current_screen_name = "daily"

        # Construct visual foundation
        self._build_layout()
        self.switch_screen("daily")

    def _build_layout(self):
        self.sidebar = Sidebar(
            parent=self.root,
            theme=self.theme,
            fonts=self.fonts,
            on_navigate=self.switch_screen,
            on_toggle_font=self._toggle_font,
            use_pixel=self.task_manager.use_pixel_font,
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.main_container = tk.Frame(self.root, bg=self.theme["bg"])
        self.main_container.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=25, pady=20
        )

    def switch_screen(self, screen_name: str):
        """Mounts the requested view inside the dynamic main container."""
        self.current_screen_name = screen_name
        self.sidebar.set_active(screen_name)

        if self.current_screen:
            self.current_screen.destroy()

        if screen_name == "daily":
            self.current_screen = DailyView(
                self.main_container, self.task_manager, self.theme, self.fonts
            )
        else:
            self.current_screen = GeneralView(
                self.main_container, self.task_manager, self.theme, self.fonts
            )

        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def _toggle_font(self):
        """Switches typography style, saves preference, and re-renders active UI."""
        new_val = not self.task_manager.use_pixel_font
        self.task_manager.use_pixel_font = new_val
        self.fonts = get_font_definitions(new_val)

        self.sidebar.update_styles(self.fonts, new_val)
        self.switch_screen(self.current_screen_name)


def main():
    # Force Per-Monitor High DPI Awareness on Windows
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