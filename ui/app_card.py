
import os
import datetime
import customtkinter as ctk
from process_runner import ProcessRunner

class AppCard(ctk.CTkFrame):
    def __init__(self, master, app_model, run_callback, edit_callback=None, delete_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.app_model = app_model
        self.run_callback = run_callback
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback

        # --- Ultra-Modern aesthetic (Zinc & Indigo) ---
        self.configure(
            fg_color="#18181b",      # Zinc-900
            border_width=1, 
            border_color="#27272a",  # Zinc-800
            corner_radius=16
        )

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) 

        # 1. Header with Icon
        self.label_name = ctk.CTkLabel(
            self, 
            text=f"📦 {self.app_model.name}",
            font=("Segoe UI", 16, "bold"),
            text_color="#fafafa", # Zinc-50
            anchor="w"
        )
        self.label_name.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")

        # 2. Subtitle: Metadata (Dense)
        # Calculate Last Modified
        try:
            mtime = os.path.getmtime(self.app_model.path)
            dt = datetime.datetime.fromtimestamp(mtime).strftime("%b %d, %H:%M")
        except:
            dt = "Unknown"

        self.label_detail = ctk.CTkLabel(
            self, 
            text=f"{self.app_model.entry_point}  •  Updated {dt}",
            font=("Segoe UI", 12),
            text_color="#71717a", # Zinc-500
            anchor="w"
        )
        self.label_detail.grid(row=1, column=0, padx=24, pady=(0, 15), sticky="ew")

        # 3. Utility Actions (Row 2) - Small Ghost Buttons
        self.util_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.util_frame.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # Open Folder
        self.btn_folder = ctk.CTkButton(
            self.util_frame,
            text="📂 Folder",
            font=("Segoe UI", 11, "bold"),
            width=80,
            height=28,
            fg_color="#27272a",    # Zinc-800
            hover_color="#3f3f46",
            text_color="#d4d4d8",  # Zinc-300
            corner_radius=14,
            command=self.open_folder
        )
        self.btn_folder.pack(side="left", padx=(0, 8))

        # Edit Code
        self.btn_edit = ctk.CTkButton(
            self.util_frame,
            text="📝 Edit",
            font=("Segoe UI", 11, "bold"),
            width=70,
            height=28,
            fg_color="transparent",
            border_width=1,
            border_color="#3f3f46",
            hover_color="#27272a",
            text_color="#a1a1aa",
            corner_radius=14,
            command=self.edit_code
        )
        self.btn_edit.pack(side="left")

        # Configure/Override (Gear Icon)
        if self.edit_callback:
            self.btn_config = ctk.CTkButton(
                self.util_frame,
                text="⚙️",
                font=("Segoe UI", 12),
                width=30,
                height=28,
                fg_color="transparent",
                hover_color="#27272a",
                text_color="#a1a1aa",
                corner_radius=14,
                command=self.on_configure
            )
            self.btn_config.pack(side="right", padx=(5, 0))

        # Delete (Trash Icon)
        if self.delete_callback:
            self.btn_delete = ctk.CTkButton(
                self.util_frame,
                text="🗑️",
                font=("Segoe UI", 12),
                width=30,
                height=28,
                fg_color="transparent",
                hover_color="#ef4444", # Red hover
                text_color="#a1a1aa",
                corner_radius=14,
                command=self.on_delete
            )
            self.btn_delete.pack(side="right", padx=(5, 0))

        # 4. Primary Actions (Row 3)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)

        # Primary: Launch (Pill Shaped, Indigo)
        self.btn_run = ctk.CTkButton(
            self.btn_frame,
            text="🚀 Launch",
            font=("Segoe UI", 13, "bold"),
            command=self.on_run,
            fg_color="#6366f1",    # Indigo-500
            hover_color="#4f46e5", # Indigo-600
            text_color="white",
            height=40,
            corner_radius=20
        )
        self.btn_run.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        # Secondary: Admin
        self.btn_admin = ctk.CTkButton(
            self.btn_frame,
            text="⚡ Admin",
            font=("Segoe UI", 12, "bold"),
            command=self.on_run_admin,
            fg_color="#27272a",    # Zinc-800
            hover_color="#ef4444", # Red
            text_color="#e4e4e7",
            height=40,
            corner_radius=20
        )
        self.btn_admin.grid(row=0, column=1, sticky="ew")

    def on_run(self):
        self.run_callback(self.app_model, as_admin=False)

    def on_run_admin(self):
        self.run_callback(self.app_model, as_admin=True)

    def open_folder(self):
        ProcessRunner.open_directory(self.app_model.path)

    def on_configure(self):
        if self.edit_callback:
            self.edit_callback(self.app_model)

    def on_delete(self):
        if self.delete_callback:
            self.delete_callback(self.app_model)

    def edit_code(self):
        script_path = os.path.join(self.app_model.path, self.app_model.entry_point)
        ProcessRunner.open_in_editor(script_path)
