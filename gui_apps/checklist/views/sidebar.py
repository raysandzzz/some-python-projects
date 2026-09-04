"""Sidebar navigation component and font toggle control."""

import tkinter as tk


class Sidebar(tk.Frame):

    def __init__(
        self,
        parent,
        theme: dict,
        fonts: dict,
        on_navigate,
        on_toggle_font,
        use_pixel: bool,
    ):
        super().__init__(
            parent, bg=theme["sidebar"], width=160, padx=14, pady=20
        )
        self.pack_propagate(False)

        self.theme = theme
        self.fonts = fonts
        self.on_navigate = on_navigate
        self.on_toggle_font = on_toggle_font

        # Discrete font toggle button at the bottom
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

        # Brand header
        self.lbl_title = tk.Label(
            self,
            text="CHECKLIST",
            font=self.fonts["sidebar_title"],
            bg=self.theme["sidebar"],
            fg=self.theme["accent"],
        )
        self.lbl_title.pack(anchor="w", pady=(0, 25))

        # Navigation buttons
        self.btn_daily = tk.Button(
            self,
            text="  Daily Tasks",
            font=self.fonts["nav"],
            bg=self.theme["sidebar"],
            fg=self.theme["text"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["accent"],
            relief=tk.FLAT,
            anchor="w",
            cursor="hand2",
            pady=6,
            command=lambda: self.on_navigate("daily"),
        )
        self.btn_daily.pack(fill=tk.X, pady=4)

        self.btn_general = tk.Button(
            self,
            text="  General",
            font=self.fonts["nav"],
            bg=self.theme["sidebar"],
            fg=self.theme["muted"],
            activebackground=self.theme["btn_active"],
            activeforeground=self.theme["text"],
            relief=tk.FLAT,
            anchor="w",
            cursor="hand2",
            pady=6,
            command=lambda: self.on_navigate("general"),
        )
        self.btn_general.pack(fill=tk.X, pady=4)

    def set_active(self, view_name: str):
        """Highlights the button matching the currently visible screen."""
        if view_name == "daily":
            self.btn_daily.config(
                fg=self.theme["accent"], bg=self.theme["card"]
            )
            self.btn_general.config(
                fg=self.theme["muted"], bg=self.theme["sidebar"]
            )
        else:
            self.btn_daily.config(
                fg=self.theme["muted"], bg=self.theme["sidebar"]
            )
            self.btn_general.config(
                fg=self.theme["accent"], bg=self.theme["card"]
            )

    def update_styles(self, fonts: dict, use_pixel: bool):
        """Refreshes typography references across sidebar controls."""
        self.fonts = fonts
        self.lbl_title.config(font=self.fonts["sidebar_title"])
        self.btn_daily.config(font=self.fonts["nav"])
        self.btn_general.config(font=self.fonts["nav"])
        self.btn_toggle_font.config(
            text="Font: Pixel" if use_pixel else "Font: Clean",
            font=self.fonts["footer"],
        )