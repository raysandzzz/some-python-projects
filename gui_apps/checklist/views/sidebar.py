"""Sidebar navigation component and font toggle control."""

import tkinter as tk
from tkinter import messagebox


class Sidebar(tk.Frame):

    def __init__(
        self,
        parent,
        task_manager,
        theme: dict,
        fonts: dict,
        on_navigate,
        on_toggle_font,
        use_pixel: bool,
    ):
        # Ancho fijo bloqueado a 220px para que no empuje el contenido derecho
        super().__init__(
            parent, bg=theme["sidebar"], width=220, padx=14, pady=20
        )
        self.pack_propagate(False)

        self.task_manager = task_manager
        self.theme = theme
        self.fonts = fonts
        self.on_navigate = on_navigate
        self.on_toggle_font = on_toggle_font

        self.active_screen = "daily"
        self.active_list = "General"
        self.is_expanded = True
        self.entry_new_list = None
        self.sublist_buttons = {}

        # Botón de tipografía inferior
        initial_text = "Font: Pixel" if use_pixel else "Font: Clean"
        self.btn_toggle_font = tk.Button(
            self,
            text=initial_text,
            font=self.fonts["footer"],
            bg=self.theme["sidebar"],
            fg=self.theme["muted"],
            activebackground=self.theme["sidebar"],
            activeforeground=self.theme["accent"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            anchor="w",
            command=self.on_toggle_font,
        )
        self.btn_toggle_font.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Título superior
        self.lbl_title = tk.Label(
            self,
            text="CHECKLIST",
            font=self.fonts["sidebar_title"],
            bg=self.theme["sidebar"],
            fg=self.theme["accent"],
        )
        self.lbl_title.pack(anchor="w", pady=(0, 20))

        # Contenedor con scroll para la navegación
        self.scroll_container = tk.Frame(self, bg=self.theme["sidebar"])
        self.scroll_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.scroll_container,
            bg=self.theme["sidebar"],
            highlightthickness=0,
            bd=0,
            width=190,
        )
        self.scrollbar = tk.Scrollbar(
            self.scroll_container,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
            width=5,
            bd=0,
            relief=tk.FLAT,
        )

        self.nav_content = tk.Frame(self.canvas, bg=self.theme["sidebar"])
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.nav_content, anchor="nw"
        )

        self.nav_content.bind("<Configure>", self._on_content_configure)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón Daily
        self.btn_daily = tk.Button(
            self.nav_content,
            text="Daily Tasks",
            font=self.fonts["nav"],
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["accent"],
            relief=tk.FLAT,
            anchor="w",
            cursor="hand2",
            padx=10,
            pady=6,
            command=lambda: self.on_navigate("daily"),
        )
        self.btn_daily.pack(fill=tk.X, pady=4)

        # Fila General + Botón '+'
        self.general_header_frame = tk.Frame(self.nav_content, bg=self.theme["sidebar"])
        self.general_header_frame.pack(fill=tk.X, pady=4)

        self.btn_general = tk.Button(
            self.general_header_frame,
            text="General ▾",
            font=self.fonts["nav"],
            bg=self.theme["sidebar"],
            fg=self.theme["muted"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["text"],
            relief=tk.FLAT,
            anchor="w",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self._on_click_general_parent,
        )
        self.btn_general.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_add_sublist = tk.Button(
            self.general_header_frame,
            text="+",
            font=self.fonts["btn"],
            bg=self.theme["sidebar"],
            fg=self.theme["accent"],
            activebackground=self.theme["card"],
            activeforeground=self.theme["accent"],
            relief=tk.FLAT,
            cursor="hand2",
            padx=6,
            pady=2,
            command=self._show_new_list_input,
        )
        self.btn_add_sublist.pack(side=tk.RIGHT)

        # Contenedor de sublistas
        self.sublists_container = tk.Frame(self.nav_content, bg=self.theme["sidebar"])
        self.sublists_container.pack(fill=tk.X)

        self.render_sublists()

        # Listeners para scroll del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.canvas.bind_all("<Button-4>", lambda e: self._scroll_sidebar(-1), add="+")
        self.canvas.bind_all("<Button-5>", lambda e: self._scroll_sidebar(1), add="+")

    def _is_hovered(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        target = widget
        while target:
            if target == self.scroll_container or target == self:
                return True
            target = getattr(target, "master", None)
        return False

    def _on_mousewheel(self, event):
        if self._is_hovered(event):
            self._scroll_sidebar(int(-1 * (event.delta / 120)))

    def _scroll_sidebar(self, units: int):
        bbox = self.canvas.bbox("all")
        if bbox and (bbox[3] - bbox[1]) > self.canvas.winfo_height():
            self.canvas.yview_scroll(units, "units")

    def _on_content_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        bbox = self.canvas.bbox("all")
        if bbox and (bbox[3] - bbox[1]) > self.canvas.winfo_height():
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.scrollbar.pack_forget()

    def _on_click_general_parent(self):
        self.is_expanded = not self.is_expanded
        arrow = "▾" if self.is_expanded else "▸"
        self.btn_general.config(text=f"General {arrow}")

        if self.is_expanded:
            self.sublists_container.pack(fill=tk.X)
        else:
            self.sublists_container.pack_forget()

        self.on_navigate("general", "General")

    def render_sublists(self):
        for w in self.sublists_container.winfo_children():
            if w != self.entry_new_list:
                w.destroy()

        self.sublist_buttons.clear()
        lists = self.task_manager.get_general_list_names()

        for name in lists:
            if name == "General":
                continue

            btn = tk.Button(
                self.sublists_container,
                text=f"- {name}",
                font=self.fonts["body"],
                bg=self.theme["sidebar"],
                fg=self.theme["muted"],
                activebackground=self.theme["btn_active"],
                activeforeground=self.theme["text"],
                relief=tk.FLAT,
                anchor="w",
                cursor="hand2",
                padx=16,
                pady=3,
                command=lambda n=name: self.on_navigate("general", n),
            )
            btn.pack(fill=tk.X, pady=1)

            btn.bind("<Button-3>", lambda e, n=name: self._confirm_delete_list(n))
            btn.bind("<Button-2>", lambda e, n=name: self._confirm_delete_list(n))

            self.sublist_buttons[name] = btn

    def _confirm_delete_list(self, name: str):
        confirm = messagebox.askyesno(
            title="Delete List",
            message=f"Are you sure you want to delete '{name}' and all of its tasks?",
            parent=self.winfo_toplevel(),
        )
        if confirm:
            self.task_manager.delete_general_list(name)
            self.render_sublists()
            if self.active_list == name:
                self.on_navigate("general", "General")

    def _show_new_list_input(self):
        if not self.is_expanded:
            self.is_expanded = True
            self.btn_general.config(text="General ▾")
            self.sublists_container.pack(fill=tk.X)

        if self.entry_new_list:
            self.entry_new_list.focus_set()
            return

        self.entry_new_list = tk.Entry(
            self.sublists_container,
            font=self.fonts["body"],
            bg=self.theme["card"],
            fg=self.theme["text"],
            insertbackground=self.theme["accent"],
            relief=tk.FLAT,
        )
        self.entry_new_list.pack(fill=tk.X, padx=(16, 5), pady=4, ipady=3)
        self.entry_new_list.focus_set()

        self.entry_new_list.bind("<Return>", lambda e: self._save_new_list())
        self.entry_new_list.bind("<Escape>", lambda e: self._cancel_new_list())

        self.after(50, lambda: self.canvas.yview_moveto(1.0))

    def _save_new_list(self):
        name = self.entry_new_list.get().strip()
        if name:
            self.task_manager.create_general_list(name)
            self._cancel_new_list()
            self.render_sublists()
            self.on_navigate("general", name)
        else:
            self._cancel_new_list()

    def _cancel_new_list(self):
        if self.entry_new_list:
            self.entry_new_list.destroy()
            self.entry_new_list = None

    def set_active(self, view_name: str, list_name: str = "General"):
        self.active_screen = view_name
        self.active_list = list_name

        if view_name == "daily":
            self.btn_daily.config(fg=self.theme["accent"], bg=self.theme["card"])
            self.btn_general.config(fg=self.theme["muted"], bg=self.theme["sidebar"])
        else:
            self.btn_daily.config(fg=self.theme["muted"], bg=self.theme["sidebar"])
            if list_name == "General":
                self.btn_general.config(fg=self.theme["accent"], bg=self.theme["card"])
            else:
                self.btn_general.config(fg=self.theme["text"], bg=self.theme["sidebar"])

        for name, btn in self.sublist_buttons.items():
            if view_name == "general" and list_name == name:
                btn.config(fg=self.theme["accent"], bg=self.theme["card"])
            else:
                btn.config(fg=self.theme["muted"], bg=self.theme["sidebar"])

    def update_styles(self, fonts: dict, use_pixel: bool):
        self.fonts = fonts
        self.lbl_title.config(font=self.fonts["sidebar_title"])
        self.btn_daily.config(font=self.fonts["nav"])
        self.btn_general.config(font=self.fonts["nav"])
        self.btn_add_sublist.config(font=self.fonts["btn"])
        self.btn_toggle_font.config(
            text="Font: Pixel" if use_pixel else "Font: Clean",
            font=self.fonts["footer"],
        )
        for btn in self.sublist_buttons.values():
            btn.config(font=self.fonts["body"])