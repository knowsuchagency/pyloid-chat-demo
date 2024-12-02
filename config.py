from pathlib import Path
import shelve

import litellm


class Config:
    config_dir = Path.home() / ".config" / "pyloid_demo"
    config_path = config_dir / "config"
    key = "api_key"

    def __init__(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with shelve.open(str(self.config_path)) as db:
            db.setdefault(self.key, "")

    def get_api_key(self):
        try:
            with shelve.open(str(self.config_path)) as db:
                result = db.get(self.key, "")
                litellm.api_key = result
                return result
        except Exception:
            return ""

    def set_api_key(self, value):
        with shelve.open(str(self.config_path)) as db:
            db[self.key] = value
            litellm.api_key = value
