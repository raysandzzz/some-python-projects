"""Persistent general tasks backlog view."""

import tkinter as tk


class GeneralView(tk.Frame):

    def __init__(
        self,
        parent,
        task_manager,
        theme: dict,
        fonts: dict,
        active_list: str = "General",
    ):
        super().__init__(parent, bg=theme["bg"])
        self.task_manager = task_manager
        self.theme = theme
        self.fonts = fonts
        self.active_list = active_list

        self._build_header()
        self._build_entry_bar()
        self._build_scrollable_list()

        # Etiqueta estática de lista vacía (FUERA del canvas)
        self.empty_lbl = tk.Label(
            self,
            font=self.fonts["subtitle"],
            bg=self.theme["bg"],
            fg=self.theme["muted"],
            justify="center",
            pady=40,
        )

        self.render_tasks()

    def _build_header(self):
        header = tk.Frame(self, bg=self.theme["bg"])
        header.pack(fill=tk.X, pady=(0, 15))

        lbl_title = tk.Label(
            header,
            text=f"{self.active_list} Backlog",
            font=self.fonts["title"],
            bg=self.theme["bg"],
            fg=self.theme["text"],
        )
        lbl_title.pack(anchor="w")

        lbl_desc = tk.Label(
            header,
            text=f"Checklist for {self.active_list.lower()} goals.",
            font=self.fonts["subtitle"],
            bg=self.theme["bg"],
            fg=self.theme["muted"],
        )
        lbl_desc.pack(anchor="w")

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
            text="Add Task",
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
        self.container_outer = tk.Frame(self, bg=self.theme["bg"])
        self.container_outer.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.container_outer,
            bg=self.theme["bg"],
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = tk.Scrollbar(
            self.container_outer,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
        )

        self.list_container = tk.Frame(self.canvas, bg=self.theme["bg"])
        self.list_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.list_container, anchor="nw"
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Eventos de scroll verificando el cursor
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.canvas.bind_all("<Button-4>", lambda e: self._scroll_main(-1), add="+")
        self.canvas.bind_all("<Button-5>", lambda e: self._scroll_main(1), add="+")

    def _is_hovered(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        target = widget
        while target:
            if target == self.container_outer:
                return True
            target = getattr(target, "master", None)
        return False

    def _on_mousewheel(self, event):
        if self._is_hovered(event):
            self._scroll_main(int(-1 * (event.delta / 120)))

    def _scroll_main(self, units: int):
        bbox = self.canvas.bbox("all")
        if bbox and (bbox[3] - bbox[1]) > self.canvas.winfo_height():
            self.canvas.yview_scroll(units, "units")

    def render_tasks(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        tasks = self.task_manager.get_general_tasks(self.active_list)
        
        if not tasks:
            # Ocultamos el canvas para que sea imposible scrollear y mostramos el label estático
            self.container_outer.pack_forget()
            self.empty_lbl.config(
                text=f"No tasks in '{self.active_list}' right now.\nAdd any pending items above."
            )
            self.empty_lbl.pack(fill=tk.BOTH, expand=True)
            return

        # Si hay tareas, aseguramos que el canvas esté visible y el label oculto
        self.empty_lbl.pack_forget()
        self.container_outer.pack(fill=tk.BOTH, expand=True)

        total = len(tasks)
        for display_idx, task in enumerate(reversed(tasks)):
            orig_idx = total - 1 - display_idx

            row = tk.Frame(self.list_container, bg=self.theme["card"], pady=6)
            row.pack(fill=tk.X, pady=4)

            status_symbol = "✓" if task["done"] else "○"
            status_fg = self.theme["accent"] if task["done"] else self.theme["muted"]

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

            text_fg = self.theme["muted"] if task["done"] else self.theme["text"]
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
            self.task_manager.add_general_task(text, self.active_list)
            self.entry.delete(0, tk.END)
            self.render_tasks()

    def _toggle_task(self, index: int):
        self.task_manager.toggle_general_task(index, self.active_list)
        self.render_tasks()

    def _delete_task(self, index: int):
        self.task_manager.delete_general_task(index, self.active_list)
        self.render_tasks()