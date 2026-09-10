import ctypes
import os
import tkinter as tk
from tkinter import font as tkfont


def load_custom_font(font_path: str):
    """Registers a private font in Windows for the current process session."""
    if os.name == "nt" and os.path.exists(font_path):
        try:
            # 0x10 = FR_PRIVATE (process-scoped, automatically unloaded on exit)
            ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)
        except Exception:
            pass


class StopwatchApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stopwatch")

        # Theme Palette
        self.bg_color = "#181824"
        self.btn_bg = "#222334"
        self.text_main = "#cdd6f4"
        self.text_muted = "#565a75"
        self.accent_time = "#ff757f"
        self.btn_active = "#2f314c"

        self.root.configure(bg=self.bg_color)
        self.root.resizable(False, False)

        # State vars
        self.running = False
        self.elapsed_seconds = 0
        self._job = None

        # Resolve available fonts with fallback
        self._resolve_fonts()
        self._build_ui()

    def _resolve_fonts(self):
        # Optional: load local .ttf if placed alongside the script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_file = os.path.join(base_dir, "Minecraft.ttf")
        if os.path.exists(font_file):
            load_custom_font(font_file)

        installed_fonts = [f.lower() for f in tkfont.families(self.root)]

        # Select primary font or fall back to standard scalable monospaced fonts
        if "minecraft" in installed_fonts:
            self.font_family = "Minecraft"
            self.time_size = 32
            self.btn_size = 10
        elif "consolas" in installed_fonts:
            self.font_family = "Consolas"
            self.time_size = 34
            self.btn_size = 10
        else:
            self.font_family = "Courier New"
            self.time_size = 32
            self.btn_size = 10

    def _build_ui(self):
        container = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=24)
        container.pack()

        self.label_time = tk.Label(
            container,
            text="00:00:00",
            font=(self.font_family, self.time_size, "bold"),
            bg=self.bg_color,
            fg=self.accent_time,
            pady=15,
        )
        self.label_time.pack()

        btn_frame = tk.Frame(container, bg=self.bg_color)
        btn_frame.pack(pady=(10, 0))

        btn_font = (self.font_family, self.btn_size, "bold")

        self.btn_start = tk.Button(
            btn_frame,
            text="Start",
            width=8,
            height=2,
            font=btn_font,
            bg=self.btn_bg,
            fg=self.text_main,
            activebackground=self.btn_active,
            activeforeground=self.text_main,
            disabledforeground=self.text_muted,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start,
        )
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(
            btn_frame,
            text="Pause",
            width=8,
            height=2,
            font=btn_font,
            bg=self.btn_bg,
            fg=self.text_main,
            activebackground=self.btn_active,
            activeforeground=self.text_main,
            disabledforeground=self.text_muted,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.pause,
        )
        self.btn_pause.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(
            btn_frame,
            text="Reset",
            width=8,
            height=2,
            font=btn_font,
            bg=self.btn_bg,
            fg=self.text_main,
            activebackground=self.btn_active,
            activeforeground=self.text_main,
            disabledforeground=self.text_muted,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.reset,
        )
        self.btn_reset.grid(row=0, column=2, padx=5)

    def _format_time(self, total_seconds: int) -> str:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _update_clock(self):
        if self.running:
            self.elapsed_seconds += 1
            self.label_time.config(text=self._format_time(self.elapsed_seconds))
            self._job = self.root.after(1000, self._update_clock)

    def start(self):
        if not self.running:
            self.running = True
            self.btn_start.config(state=tk.DISABLED)
            self.btn_pause.config(state=tk.NORMAL)
            self.btn_reset.config(state=tk.NORMAL)
            self._update_clock()

    def pause(self):
        if self.running:
            self.running = False
            if self._job:
                self.root.after_cancel(self._job)
            self.btn_start.config(state=tk.NORMAL)
            self.btn_pause.config(state=tk.DISABLED)

    def reset(self):
        self.running = False
        if self._job:
            self.root.after_cancel(self._job)
        self.elapsed_seconds = 0
        self.label_time.config(text="00:00:00")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        self.btn_reset.config(state=tk.DISABLED)


def main():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

    root = tk.Tk()
    StopwatchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()