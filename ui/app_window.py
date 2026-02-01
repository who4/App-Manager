
import threading
import queue
import customtkinter as ctk
from tkinter import filedialog
import os

from config_manager import ConfigManager
from app_scanner import AppScanner, AppModel
from process_runner import ProcessRunner
from ui.dashboard import Dashboard
from ui.add_app_dialog import AddAppDialog

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("App Manager Logic")
        self.geometry("1200x600")
        
        # Configure Theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # State
        self.current_path = ConfigManager.get_root_dir()
        self.scan_queue = queue.Queue()
        
        if self.current_path and os.path.exists(self.current_path):
            self.show_dashboard()
        else:
            self.show_setup()

    def show_setup(self):
        self.clear_container()
        
        frame = ctk.CTkFrame(self.main_container)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        lbl = ctk.CTkLabel(frame, text="Select your Projects Directory", font=("Roboto", 20))
        lbl.pack(padx=40, pady=(40, 20))

        btn = ctk.CTkButton(frame, text="Browse Folder", command=self.select_directory)
        btn.pack(padx=40, pady=(0, 40))

    def show_dashboard(self):
        self.clear_container()

        # Top Bar: Seamless, transparent feel
        top_bar = ctk.CTkFrame(
            self.main_container, 
            height=100, 
            fg_color="#09090b", # Zinc-950 (Seamless)
            corner_radius=0
        )
        top_bar.pack(side="top", fill="x", pady=(10, 0))

        # 1. Branding / Title (Left)
        title_lbl = ctk.CTkLabel(
            top_bar, 
            text="App Manager", 
            font=("Segoe UI", 28, "bold"),
            text_color="#fafafa"
        )
        title_lbl.pack(side="left", padx=40, pady=30)

        # 2. Path Display (Next to title, but subtle)
        path_lbl = ctk.CTkLabel(
            top_bar, 
            text=f"📂 {self.current_path}", 
            text_color="#52525b", # Zinc-600
            font=("Segoe UI", 14)
        )
        path_lbl.pack(side="left", padx=20, pady=34)

        # 3. Actions (Right Aligned)
        
        # Add Custom App (Solid Pill)
        add_btn = ctk.CTkButton(
            top_bar,
            text="➕ Add App",
            font=("Segoe UI", 13, "bold"),
            width=110,
            height=42,
            corner_radius=21,
            fg_color="#10b981", # Emerald-500
            hover_color="#059669",
            text_color="white",
            command=self.add_custom_app
        )
        add_btn.pack(side="right", padx=(0, 40), pady=30)

        # Refresh (Vibrant Pill)
        refresh_btn = ctk.CTkButton(
            top_bar, 
            text="🔄 Refresh",
            font=("Segoe UI", 13, "bold"),
            width=130, 
            height=42,
            corner_radius=21,
            fg_color="#6366f1", # Indigo-500
            hover_color="#4f46e5",
            text_color="white",
            command=self.refresh_dashboard
        )
        refresh_btn.pack(side="right", padx=(0, 15), pady=30)

        # Change Dir (Ghost/Outline Pill)
        change_dir_btn = ctk.CTkButton(
            top_bar, 
            text="📁 Change", 
            font=("Segoe UI", 13, "bold"),
            width=110, 
            height=42,
            corner_radius=21,
            fg_color="transparent", 
            border_width=2,
            border_color="#27272a", # Zinc-800
            hover_color="#27272a",
            text_color="#a1a1aa",   # Zinc-400
            command=self.select_directory
        )
        change_dir_btn.pack(side="right", padx=(0, 15), pady=30)

        # Content - Loading State
        self.loading_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.loading_frame.pack(expand=True, fill="both")
        
        self.loading_lbl = ctk.CTkLabel(
            self.loading_frame, 
            text="Scanning...", 
            font=("Segoe UI", 18),
            text_color="#52525b"
        )
        self.loading_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Run scan in thread
        threading.Thread(target=self.run_scan, args=(self.current_path,), daemon=True).start()
        self.after(100, self.check_scan_queue)

    def run_scan(self, path):
        apps = AppScanner.scan(path)
        
        # Load manual apps
        manual_apps_data = ConfigManager.get_manual_apps()
        for app_data in manual_apps_data:
            # Avoid duplicates if they are already in scanned apps (by path)
            if not any(existing.path == app_data["path"] for existing in apps):
                apps.append(AppModel(
                    name=app_data["name"],
                    path=app_data["path"],
                    entry_point=app_data["entry_point"]
                ))
        
        self.scan_queue.put(apps)

    def check_scan_queue(self):
        try:
            apps = self.scan_queue.get_nowait()
            # Scan complete
            if hasattr(self, 'loading_frame'):
                self.loading_frame.destroy()
            
            if hasattr(self, 'loading_frame'):
                self.loading_frame.destroy()
            
            self.dashboard = Dashboard(
                self.main_container, 
                apps, 
                self.run_app, 
                edit_callback=self.edit_entry_point,
                delete_callback=self.delete_app
            )
            self.dashboard.pack(fill="both", expand=True, padx=40, pady=20)
            
        except queue.Empty:
            # Check again soon
            self.after(100, self.check_scan_queue)

    def select_directory(self):
        path = filedialog.askdirectory()
        if path:
            ConfigManager.set_root_dir(path)
            self.current_path = path
            self.show_dashboard()

    def refresh_dashboard(self):
        # Simply reload the whole dashboard to ensure clean state and correct packing order
        if self.current_path:
            self.show_dashboard()

    def add_custom_app(self):
        # Open Dialog
        AddAppDialog(self, callback=self.on_app_added)

    def on_app_added(self, app_data):
        # Save to config
        ConfigManager.add_manual_app(app_data)
        
        # Refresh
        self.refresh_dashboard()

    def edit_entry_point(self, app_model):
        # Open file dialog startign at app path
        initial_dir = app_model.path
        if not os.path.exists(initial_dir):
            initial_dir = self.current_path

        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title=f"Select Entry Point for {app_model.name}",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )

        if file_path:
            # check if inside the app folder (preferred but not strictly required by logic, 
            # but good validation to ensure we're editing the right app)
            # actually, we just take the basename.
            
            new_entry = os.path.basename(file_path)
            # Store override
            ConfigManager.add_app_override(app_model.path, new_entry)
            
            self.refresh_dashboard()

    def delete_app(self, app_model):
        # Check if it was a manual app
        manual_apps = ConfigManager.get_manual_apps()
        is_manual = any(app["path"] == app_model.path for app in manual_apps)

        if is_manual:
            ConfigManager.remove_manual_app(app_model.path)
        else:
            # It's an auto-scanned app -> add to ignore list
            ConfigManager.add_ignored_app(app_model.path)
        
        self.refresh_dashboard()

    def run_app(self, app_model, as_admin):
        print(f"Running {app_model.name} (Admin: {as_admin})...")
        ProcessRunner.run_app(app_model, as_admin)

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = AppWindow()
    # Apply background to root
    app.configure(fg_color="#09090b") 
    app.mainloop()
