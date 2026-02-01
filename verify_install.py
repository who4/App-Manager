
import sys
import os

try:
    print("Checking imports...")
    import customtkinter
    print("customtkinter imported.")
    import config_manager
    print("config_manager imported.")
    import app_scanner
    print("app_scanner imported.")
    import process_runner
    print("process_runner imported.")
    from ui.app_window import AppWindow
    print("AppWindow imported.")
    print("All checks passed.")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)
