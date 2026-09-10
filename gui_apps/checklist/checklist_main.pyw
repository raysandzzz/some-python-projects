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

        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "check_icon.png")
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, self.icon)

        self.task_manager = TaskManager(os.path.join(base_dir, "tasks.json"))
        self.theme = THEMES["dark"]
        self.root.configure(bg=self.theme["bg"])
        self.fonts = get_font_definitions(self.task_manager.use_pixel_font)

        self.current_screen = None
        self.current_screen_name = "daily"
        self.current_list_name = "General"

        self._build_layout()
        self.switch_screen("daily")

    def _build_layout(self):
        self.sidebar = Sidebar(
            parent=self.root,
            task_manager=self.task_manager,
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

    def switch_screen(self, screen_name: str, list_name: str = "General"):
        """Monta la vista solicitada y resalta la selección en el sidebar."""
        self.current_screen_name = screen_name
        self.current_list_name = list_name
        self.sidebar.set_active(screen_name, list_name)

        if self.current_screen:
            self.current_screen.destroy()

        if screen_name == "daily":
            self.current_screen = DailyView(
                self.main_container, self.task_manager, self.theme, self.fonts
            )
        else:
            self.current_screen = GeneralView(
                self.main_container,
                self.task_manager,
                self.theme,
                self.fonts,
                active_list=list_name,
            )

        self.current_screen.pack(fill=tk.BOTH, expand=True)

    def _toggle_font(self):
        new_val = not self.task_manager.use_pixel_font
        self.task_manager.use_pixel_font = new_val
        self.fonts = get_font_definitions(new_val)

        self.sidebar.update_styles(self.fonts, new_val)
        self.switch_screen(self.current_screen_name, self.current_list_name)


def main():
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