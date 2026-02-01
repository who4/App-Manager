
import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    @staticmethod
    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except:
                return {"manual_apps": [], "app_overrides": {}, "ignored_apps": []}
        return {"manual_apps": [], "app_overrides": {}, "ignored_apps": []}

    @staticmethod
    def save_config(data):
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def get_root_dir():
        config = ConfigManager.load_config()
        return config.get("root_dir")

    @staticmethod
    def set_root_dir(path):
        config = ConfigManager.load_config()
        config["root_dir"] = path
        ConfigManager.save_config(config)

    @staticmethod
    def get_manual_apps():
        config = ConfigManager.load_config()
        return config.get("manual_apps", [])

    @staticmethod
    def add_manual_app(app_data):
        config = ConfigManager.load_config()
        if "manual_apps" not in config:
            config["manual_apps"] = []
        
        # Check for duplicates by path
        if not any(app["path"] == app_data["path"] for app in config["manual_apps"]):
            config["manual_apps"].append(app_data)
            ConfigManager.save_config(config)

    @staticmethod
    def get_app_overrides():
        config = ConfigManager.load_config()
        return config.get("app_overrides", {})

    @staticmethod
    def add_app_override(app_path, new_entry_point):
        config = ConfigManager.load_config()
        if "app_overrides" not in config:
            config["app_overrides"] = {}
        
        config["app_overrides"][str(app_path)] = new_entry_point
        ConfigManager.save_config(config)

    @staticmethod
    def remove_manual_app(path):
        config = ConfigManager.load_config()
        if "manual_apps" in config:
            config["manual_apps"] = [app for app in config["manual_apps"] if app["path"] != path]
            ConfigManager.save_config(config)

    @staticmethod
    def get_ignored_apps():
        config = ConfigManager.load_config()
        return config.get("ignored_apps", [])

    @staticmethod
    def add_ignored_app(path):
        config = ConfigManager.load_config()
        if "ignored_apps" not in config:
            config["ignored_apps"] = []
        
        if path not in config["ignored_apps"]:
            config["ignored_apps"].append(path)
            ConfigManager.save_config(config)
