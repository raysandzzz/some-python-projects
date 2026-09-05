"""Persistent general tasks backlog view."""

import tkinter as tk


class GeneralView(tk.Frame):

    def __init__(self, parent, task_manager, theme: dict, fonts: dict):
        super().__init__(parent, bg=theme["bg"])
        self.task_manager = task_manager
        self.theme = theme
        self.fonts = fonts

        self._build_header()
        self._build_entry_bar()

        self.list_container = tk.Frame(self, bg=self.theme["bg"])
        self.list_container.pack(fill=tk.BOTH, expand=True)

        self.render_tasks()

    def _build_header(self):
        header = tk.Frame(self, bg=self.theme["bg"])
        header.pack(fill=tk.X, pady=(0, 15))

        lbl_title = tk.Label(
            header,
            text="GENERAL BACKLOG",
            font=self.fonts["title"],
            bg=self.theme["bg"],
            fg=self.theme["text"],
        )
        lbl_title.pack(anchor="w")

        lbl_desc = tk.Label(
            header,
            text="Persistent to-do list for pending goals and projects.",
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

    def render_tasks(self):
        """Clears and re-renders all general backlog rows."""
        for widget in self.list_container.winfo_children():
            widget.destroy()

        tasks = self.task_manager.get_general_tasks()
        if not tasks:
            empty_lbl = tk.Label(
                self.list_container,
                text="No general tasks right now.\nAdd any pending items above.",
                font=self.fonts["subtitle"],
                bg=self.theme["bg"],
                fg=self.theme["muted"],
                pady=30,
            )
            empty_lbl.pack()
            return

        for idx, task in enumerate(tasks):
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
                command=lambda i=idx: self._toggle_task(i),
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
                command=lambda i=idx: self._delete_task(i),
            )
            btn_del.pack(side=tk.RIGHT, padx=8)

    def _add_task(self):
        text = self.entry.get().strip()
        if text:
            self.task_manager.add_general_task(text)
            self.entry.delete(0, tk.END)
            self.render_tasks()

    def _toggle_task(self, index: int):
        self.task_manager.toggle_general_task(index)
        self.render_tasks()

    def _delete_task(self, index: int):
        self.task_manager.delete_general_task(index)
        self.render_tasks()