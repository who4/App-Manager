
import os
import glob
from config_manager import ConfigManager

class AppModel:
    def __init__(self, name, path, entry_point, app_type="python"):
        self.name = name
        self.path = path
        self.entry_point = entry_point
        self.app_type = app_type

    def __repr__(self):
        return f"<AppModel {self.name} ({self.entry_point})>"

class AppScanner:
    IGNORED_FOLDERS = {".git", ".idea", "__pycache__", ".vscode", "venv", ".venv", "node_modules"}
    ENTRY_POINTS = ["main.py", "app.py", "index.py", "start.py", "manage.py"]

    @staticmethod
    def scan(root_dir):
        apps = []
        if not root_dir or not os.path.isdir(root_dir):
            return apps

        overrides = ConfigManager.get_app_overrides()
        ignored = ConfigManager.get_ignored_apps()

        # List immediate subdirectories
        try:
            items = os.listdir(root_dir)
        except PermissionError:
            return apps

        for item in items:
            full_path = os.path.join(root_dir, item)
            
            # Skip ignored apps
            if full_path in ignored or item in ignored: # Check full path or folder name (just in case)
                 continue

            if os.path.isdir(full_path) and item not in AppScanner.IGNORED_FOLDERS:
                # Check for override
                entry_point = overrides.get(str(full_path))
                
                if not entry_point:
                     # Check for entry point
                    entry_point = AppScanner.detect_entry_point(full_path)
                
                if entry_point:
                    apps.append(AppModel(
                        name=item,
                        path=full_path,
                        entry_point=entry_point
                    ))
                else:
                    # Optional: Include folder even if no strict entry point is found? 
                    # The user said "detect the apps... name them as their folder"
                    # If we don't find a main.py, maybe we shouldn't list it, or list it as "Unknown".
                    # For now, let's only list if we find a likely python file to run.
                    # Or maybe just pick the first .py file if standard ones aren't found?
                    fallback = AppScanner.find_any_python_file(full_path)
                    if fallback:
                         apps.append(AppModel(
                            name=item,
                            path=full_path,
                            entry_point=fallback
                        ))
                    
        return apps

    @staticmethod
    def detect_entry_point(folder_path):
        for ep in AppScanner.ENTRY_POINTS:
            if os.path.exists(os.path.join(folder_path, ep)):
                return ep
        return None

    @staticmethod
    def find_any_python_file(folder_path):
        # Fallback: look for any .py file that isn't __init__.py
        # This might be risky, but useful for random scripts
        py_files = glob.glob(os.path.join(folder_path, "*.py"))
        for f in py_files:
            basename = os.path.basename(f)
            if basename != "__init__.py":
                return basename
        return None
