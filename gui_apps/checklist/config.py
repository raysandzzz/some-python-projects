"""Style themes and dynamic typography scaling configuration."""

THEMES = {
    "dark": {
        "bg": "#181824",
        "sidebar": "#12121b",
        "card": "#222334",
        "text": "#cdd6f4",
        "accent": "#a6e3a1",
        "muted": "#6c7086",
        "btn_active": "#2f314c",
        "danger": "#f38ba8",
    }
}


def get_font_definitions(use_pixel_font: bool) -> dict:
    """Returns typography tuples mapped to the chosen style scale."""
    if use_pixel_font:
        family = "Minecraft"
        return {
            "family": family,
            "sidebar_title": (family, 16),
            "nav": (family, 12),
            "title": (family, 24),
            "subtitle": (family, 10),
            "body": (family, 12),
            "btn": (family, 11),
            "footer": (family, 9),
        }

    family = "Segoe UI"
    return {
        "family": family,
        "sidebar_title": (family, 14, "bold"),
        "nav": (family, 11, "bold"),
        "title": (family, 22, "bold"),
        "subtitle": (family, 10),
        "body": (family, 11),
        "btn": (family, 10, "bold"),
        "footer": (family, 8),
    }