import tkinter as tk

class StopwatchApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("320x220")
        self.root.resizable(False, False)

        # Theme Palette (Seems like VS Code Dark Slate / Neon)
        self.bg_color = "#181824"
        self.btn_bg = "#222334"
        self.text_main = "#cdd6f4"
        self.text_muted = "#565a75"
        self.accent_time = "#ff757f"
        self.btn_active = "#2f314c"

        self.root.configure(bg=self.bg_color)

        # State vars
        self.running = False
        self.elapsed_seconds = 0
        self._job = None

        # UI Settings
        self._build_ui()

    def _build_ui(self):
        # Time display text
        self.label_time = tk.Label(
            self.root,
            text="00:00:00",
            font=("Minecraft", 36, "bold"),  # Minecraft text font XD
            bg=self.bg_color,
            fg=self.accent_time,
            pady=40
        )
        self.label_time.pack()
        
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=0)

        # .-.-.-. Buttons settings .-.-.-.
        self.btn_start = tk.Button(
            btn_frame,
            text="Start",
            width=9,
            height=2,
            font=("Minecraft", 10, "bold"),
            bg=self.btn_bg,
            fg=self.text_main,
            activebackground=self.btn_active,
            activeforeground=self.text_main,
            disabledforeground=self.text_muted,
            relief=tk.FLAT,
            command=self.start
        )
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(
            btn_frame,
            text="Pause",
            width=9,
            height=2,
            font=("Minecraft", 10, "bold"),
            bg=self.btn_bg,
            fg=self.text_main,
            activebackground=self.btn_active,
            activeforeground=self.text_main,
            disabledforeground=self.text_muted,
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self.pause
        )
        self.btn_pause.grid(row=0, column=1, padx=3)

        self.btn_reset = tk.Button(
            btn_frame,
            text="Reset",
            width=9,
            height=2,
            font=("Minecraft", 10, "bold"),
            bg=self.btn_bg,
            fg=self.text_main,
            activebackground=self.btn_active,
            activeforeground=self.text_main,
            disabledforeground=self.text_muted,
            relief=tk.FLAT,
            state=tk.DISABLED,
            command=self.reset
        )
        self.btn_reset.grid(row=0, column=2, padx=5)
        # .-.-.-. Buttons settings .-.-.-.
    
    # Format time function with HH,MM & SS support  
    def _format_time(self, total_seconds: int) -> str:
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # Update clock every second and running verif
    def _update_clock(self):
        if self.running:
            self.elapsed_seconds += 1
            self.label_time.config(text=self._format_time(self.elapsed_seconds))
            # Set the next update 1000ms later (1 second)
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
    root = tk.Tk()
    StopwatchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()