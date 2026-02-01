import customtkinter as ctk
from tkinter import filedialog
import os

class AddAppDialog(ctk.CTkToplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        
        self.title("Add Custom App")
        self.geometry("500x350")
        self.resizable(False, False)
        
        # Make modal
        self.transient(master)
        self.grab_set()
        
        self.configure(fg_color="#18181b") # Zinc-900

        self.layout_ui()
        
        # Center window
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def layout_ui(self):
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            container, 
            text="Add Custom App", 
            font=("Segoe UI", 20, "bold"),
            text_color="#fafafa"
        )
        title.pack(anchor="w", pady=(0, 20))

        # --- Name ---
        lbl_name = ctk.CTkLabel(
            container, 
            text="App Name", 
            font=("Segoe UI", 13),
            text_color="#a1a1aa"
        )
        lbl_name.pack(anchor="w", pady=(0, 5))
        
        self.entry_name = ctk.CTkEntry(
            container,
            placeholder_text="e.g. My Script",
            height=40,
            fg_color="#27272a",
            border_color="#3f3f46",
            text_color="white"
        )
        self.entry_name.pack(fill="x", pady=(0, 15))

        # --- File Selection ---
        lbl_file = ctk.CTkLabel(
            container, 
            text="Entry Point File", 
            font=("Segoe UI", 13),
            text_color="#a1a1aa"
        )
        lbl_file.pack(anchor="w", pady=(0, 5))

        file_frame = ctk.CTkFrame(container, fg_color="transparent")
        file_frame.pack(fill="x", pady=(0, 20))

        self.entry_file = ctk.CTkEntry(
            file_frame,
            placeholder_text="Select a file...",
            height=40,
            fg_color="#27272a",
            border_color="#3f3f46",
            text_color="#d4d4d8"
        )
        self.entry_file.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_browse = ctk.CTkButton(
            file_frame,
            text="Browse",
            width=80,
            height=40,
            fg_color="#3f3f46",
            hover_color="#52525b",
            text_color="white",
            command=self.browse_file
        )
        btn_browse.pack(side="right")

        # --- Buttons ---
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom")

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            border_color="#3f3f46",
            text_color="#a1a1aa",
            height=40,
            command=self.destroy
        )
        btn_cancel.pack(side="left", expand=True, fill="x", padx=(0, 10))

        btn_add = ctk.CTkButton(
            btn_frame,
            text="Add App",
            fg_color="#6366f1", # Indigo-500
            hover_color="#4f46e5",
            text_color="white",
            height=40,
            command=self.on_submit
        )
        btn_add.pack(side="right", expand=True, fill="x", padx=(10, 0))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select App Entry Point",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if file_path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, file_path)
            
            # Auto populate name if empty
            current_name = self.entry_name.get()
            if not current_name.strip():
                # Use parent folder name as default app name
                folder_name = os.path.basename(os.path.dirname(file_path))
                self.entry_name.insert(0, folder_name)

    def on_submit(self):
        name = self.entry_name.get().strip()
        path = self.entry_file.get().strip()
        
        if not name:
            # Simple error indication (shake or color could be better, but print for now)
            self.entry_name.configure(border_color="#ef4444")
            return
            
        if not path or not os.path.exists(path):
            self.entry_file.configure(border_color="#ef4444")
            return
            
        # Parse path
        folder_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        
        if self.callback:
            self.callback({
                "name": name,
                "path": folder_path,
                "entry_point": file_name
            })
            
        self.destroy()
