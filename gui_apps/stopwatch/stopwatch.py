import tkinter as tk

class StopwatchApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("320x220")
        self.root.resizable(False, False)

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
            font=("Minecraft", 36, "bold"),  # Minecraft text font xD
            pady=15
            )
        
        self.label_time.pack()
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.btn_start = tk.Button(
            btn_frame,
            text="Start",
            width=8,
            font=("Helvetica", 10, "bold"),
            command=self.start,
        )
        self.btn_start.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(
            btn_frame,
            text="Pause",
            width=8,
            state=tk.DISABLED,
            command=self.pause,
        )
        
        self.btn_pause.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(
            btn_frame,
            text="Reset",
            width=8,
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