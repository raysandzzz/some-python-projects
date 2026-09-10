"""Daily habit tracking screen with dynamic English date formatting."""

import datetime
import tkinter as tk


class DailyView(tk.Frame):

    def __init__(self, parent, task_manager, theme: dict, fonts: dict):
        super().__init__(parent, bg=theme["bg"])
        self.task_manager = task_manager
        self.theme = theme
        self.fonts = fonts

        self._build_header()
        self._build_entry_bar()
        self._build_scrollable_list()

        self.render_tasks()

    def _build_header(self):
        now = datetime.datetime.now()
        day_str = now.strftime("%A").upper()
        date_str = now.strftime("%B %d, %Y")

        header = tk.Frame(self, bg=self.theme["bg"])
        header.pack(fill=tk.X, pady=(0, 15))

        lbl_day = tk.Label(
            header,
            text=day_str,
            font=self.fonts["title"],
            bg=self.theme["bg"],
            fg=self.theme["accent"],
        )
        lbl_day.pack(anchor="w")

        lbl_date = tk.Label(
            header,
            text=date_str,
            font=self.fonts["subtitle"],
            bg=self.theme["bg"],
            fg=self.theme["muted"],
        )
        lbl_date.pack(anchor="w")

    def _build_entry_bar(self):
        entry_frame = tk.Frame(self, bg=self.theme["bg"])
        entry_frame.pack(fill=tk.X, pady=(5, 15))

        self.entry = tk.Entry(
            entry_frame,
            font=self.fonts["body"],
            bg=self.theme["card"],
            fg=self.theme["text"],
            insertbackground=self.theme["accent"],
            relief=tk.FLAT,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.entry.bind("<Return>", lambda event: self._add_task())

        btn_add = tk.Button(
            entry_frame,
            text="Add Habit",
            font=self.fonts["btn"],
            bg=self.theme["accent"],
            fg=self.theme["sidebar"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["text"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._add_task,
        )
        btn_add.pack(side=tk.RIGHT, padx=(8, 0))

    def _build_scrollable_list(self):
        """Prepara el Canvas y Scrollbar para permitir desplazamiento vertical."""
        container_outer = tk.Frame(self, bg=self.theme["bg"])
        container_outer.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            container_outer,
            bg=self.theme["bg"],
            highlightthickness=0,
            bd=0,
        )
        scrollbar = tk.Scrollbar(
            container_outer,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
        )

        self.list_container = tk.Frame(self.canvas, bg=self.theme["bg"])

        # Actualiza el tamaño de la región de desplazamiento al añadir elementos
        self.list_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.list_container, anchor="nw"
        )

        # Ajusta el ancho interno al ancho visible del canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Soporte para la rueda del ratón (Windows, macOS y Linux)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def render_tasks(self):
        """Limpia y re-renderiza los hábitos diarios colocando los más recientes arriba."""
        for widget in self.list_container.winfo_children():
            widget.destroy()

        tasks = self.task_manager.get_daily_tasks()
        if not tasks:
            empty_lbl = tk.Label(
                self.list_container,
                text="No daily habits registered yet.\nAdd one above to track it every day.",
                font=self.fonts["subtitle"],
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                pady=30,
            )
            empty_lbl.pack()
            return

        total = len(tasks)
        # Recorrido inverso manteniendo la referencia exacta del índice original
        for display_idx, task in enumerate(reversed(tasks)):
            orig_idx = total - 1 - display_idx

            row = tk.Frame(self.list_container, bg=self.theme["card"], pady=6)
            row.pack(fill=tk.X, pady=4)

            status_symbol = "✓" if task["done"] else "○"
            status_fg = (
                self.theme["accent"] if task["done"] else self.theme["muted"]
            )

            btn_toggle = tk.Button(
                row,
                text=status_symbol,
                font=self.fonts["nav"],
                width=3,
                bg=self.theme["card"],
                fg=status_fg,
                activebackground=self.theme["card"],
                activeforeground=self.theme["accent"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda i=orig_idx: self._toggle_task(i),
            )
            btn_toggle.pack(side=tk.LEFT, padx=(6, 8))

            text_fg = (
                self.theme["muted"] if task["done"] else self.theme["text"]
            )
            lbl_text = tk.Label(
                row,
                text=task["text"],
                font=self.fonts["body"],
                bg=self.theme["card"],
                fg=text_fg,
                wraplength=340,
                justify="left",
                anchor="w",
            )
            lbl_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

            btn_del = tk.Button(
                row,
                text="✕",
                font=self.fonts["btn"],
                bg=self.theme["card"],
                fg=self.theme["danger"],
                activebackground=self.theme["card"],
                activeforeground=self.theme["danger"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda i=orig_idx: self._delete_task(i),
            )
            btn_del.pack(side=tk.RIGHT, padx=8)

    def _add_task(self):
        text = self.entry.get().strip()
        if text:
            self.task_manager.add_daily_task(text)
            self.entry.delete(0, tk.END)
            self.render_tasks()

    def _toggle_task(self, index: int):
        self.task_manager.toggle_daily_task(index)
        self.render_tasks()

    def _delete_task(self, index: int):
        self.task_manager.delete_daily_task(index)
        self.render_tasks()