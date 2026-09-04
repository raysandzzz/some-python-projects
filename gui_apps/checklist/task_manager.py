"""Data persistence and business logic for daily habits and general tasks."""

import datetime
import json
import os


class TaskManager:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.data = self._load()
        self.check_midnight_reset()

    def _load(self) -> dict:
        today_str = datetime.date.today().isoformat()
        defaults = {
            "last_date": today_str,
            "use_pixel_font": False,
            "daily_tasks": [],
            "general_tasks": [],
        }

        if not os.path.exists(self.data_path):
            return defaults

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if "use_pixel_font" not in loaded:
                    loaded["use_pixel_font"] = False
                return loaded
        except Exception:
            return defaults

    def save(self):
        """Writes in-memory task collections to disk."""
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def check_midnight_reset(self):
        """Unchecks daily habits when the recorded date does not match today."""
        today_str = datetime.date.today().isoformat()
        if self.data.get("last_date") != today_str:
            for task in self.data["daily_tasks"]:
                task["done"] = False
            self.data["last_date"] = today_str
            self.save()

    # --- Preferences ---
    @property
    def use_pixel_font(self) -> bool:
        return self.data.get("use_pixel_font", False)

    @use_pixel_font.setter
    def use_pixel_font(self, val: bool):
        self.data["use_pixel_font"] = val
        self.save()

    # --- Daily Tasks ---
    def get_daily_tasks(self) -> list:
        return self.data["daily_tasks"]

    def add_daily_task(self, text: str):
        self.data["daily_tasks"].append({"text": text, "done": False})
        self.save()

    def toggle_daily_task(self, index: int):
        self.data["daily_tasks"][index]["done"] = not self.data["daily_tasks"][
            index
        ]["done"]
        self.save()

    def delete_daily_task(self, index: int):
        self.data["daily_tasks"].pop(index)
        self.save()

    # --- General Tasks ---
    def get_general_tasks(self) -> list:
        return self.data["general_tasks"]

    def add_general_task(self, text: str):
        self.data["general_tasks"].append({"text": text, "done": False})
        self.save()

    def toggle_general_task(self, index: int):
        self.data["general_tasks"][index]["done"] = not self.data[
            "general_tasks"
        ][index]["done"]
        self.save()

    def delete_general_task(self, index: int):
        self.data["general_tasks"].pop(index)
        self.save()