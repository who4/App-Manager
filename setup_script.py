import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
import shutil
import json
import subprocess

# Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SetupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Manager Setup")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Data
        self.install_dir = os.path.join(os.environ['LOCALAPPDATA'], "AppManager")
        self.apps_dir = ""

        # UI
        self.header = ctk.CTkLabel(self, text="Install App Manager", font=("Segoe UI", 24, "bold"))
        self.header.pack(pady=(30, 20))

        # Install Location
        self.loc_frame = ctk.CTkFrame(self)
        self.loc_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(self.loc_frame, text="Installation Location:").pack(anchor="w", padx=10, pady=(10,0))
        self.loc_entry = ctk.CTkEntry(self.loc_frame)
        self.loc_entry.insert(0, self.install_dir)
        self.loc_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        ctk.CTkButton(self.loc_frame, text="...", width=40, command=self.browse_install).pack(side="right", padx=10)

        # Apps Directory
        self.apps_frame = ctk.CTkFrame(self)
        self.apps_frame.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(self.apps_frame, text="Select your Projects/Apps Folder:").pack(anchor="w", padx=10, pady=(10,0))
        self.apps_entry = ctk.CTkEntry(self.apps_frame, placeholder_text="C:/Users/YourName/Documents/Apps")
        self.apps_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        ctk.CTkButton(self.apps_frame, text="Browse", width=80, command=self.browse_apps).pack(side="right", padx=10)

        # Install Button
        self.install_btn = ctk.CTkButton(self, text="INSTALL", font=("Segoe UI", 16, "bold"), height=50, command=self.run_install)
        self.install_btn.pack(side="bottom", fill="x", padx=40, pady=40)

        self.status_lbl = ctk.CTkLabel(self, text="", text_color="yellow")
        self.status_lbl.pack(side="bottom", pady=(0, 10))

    def browse_install(self):
        d = filedialog.askdirectory(initialdir=self.install_dir)
        if d:
            self.install_dir = d
            self.loc_entry.delete(0, "end")
            self.loc_entry.insert(0, d)

    def browse_apps(self):
        d = filedialog.askdirectory()
        if d:
            self.apps_dir = d
            self.apps_entry.delete(0, "end")
            self.apps_entry.insert(0, d)

    def run_install(self):
        install_path = self.loc_entry.get()
        apps_path = self.apps_entry.get()

        if not install_path or not apps_path:
            self.status_lbl.configure(text="Please fill in all fields.")
            return

        self.install_btn.configure(state="disabled", text="Installing...")
        self.update()

        try:
            # 1. Create Install Dir
            if os.path.exists(install_path):
                # Clean install? Maybe just overwrite.
                pass
            else:
                os.makedirs(install_path, exist_ok=True)

            # 2. Extract Files
            # When frozen, files are in sys._MEIPASS/bundled_app
            # We copy 'bundled_app' content to install_path
            
            # Determine source path
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                source = os.path.join(base_path, "AppManager_Bin")
            else:
                # Debug mode (not frozen)
                source = os.path.abspath("dist/AppManager") # Assumption for testing
            
            if not os.path.exists(source):
                raise Exception(f"Source files not found at {source}")

            # Copy files
            for item in os.listdir(source):
                s = os.path.join(source, item)
                d = os.path.join(install_path, item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            # 3. Create Config
            config = {
                "root_dir": apps_path,
                "manual_apps": [],
                "app_overrides": {},
                "ignored_apps": []
            }
            with open(os.path.join(install_path, "config.json"), "w") as f:
                json.dump(config, f, indent=4)

            # 4. Create Desktop Shortcut
            self.create_shortcut(install_path)

            messagebox.showinfo("Success", "Installation Complete!")
            self.destroy()

        except Exception as e:
            self.status_lbl.configure(text=f"Error: {str(e)}")
            self.install_btn.configure(state="normal", text="INSTALL")
            print(e)
            
    def create_shortcut(self, target_dir):
        try:
            desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            lnk_path = os.path.join(desktop, "App Manager.lnk")
            target_exe = os.path.join(target_dir, "AppManager.exe")
            
            # PowerShell script to create shortcut
            ps_script = f"""
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("{lnk_path}")
            $Shortcut.TargetPath = "{target_exe}"
            $Shortcut.WorkingDirectory = "{target_dir}"
            $Shortcut.Save()
            """
            
            subprocess.run(["powershell", "-Command", ps_script], check=True)
            
        except Exception as e:
            print(f"Shortcut error: {e}")
            # Fallback or ignore


if __name__ == "__main__":
    app = SetupApp()
    app.mainloop()
