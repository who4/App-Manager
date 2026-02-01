
import customtkinter as ctk
from .app_card import AppCard

class Dashboard(ctk.CTkScrollableFrame):
    def __init__(self, master, apps, run_callback, edit_callback=None, delete_callback=None, **kwargs):
        # Premium Scrollbar Styling (Zinc Theme)
        super().__init__(
            master, 
            fg_color="transparent",
            scrollbar_button_color="#27272a", 
            scrollbar_button_hover_color="#3f3f46", 
            **kwargs
        )
        self.apps = apps
        self.run_callback = run_callback
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        # Grid Layout
        self.grid_columnconfigure((0, 1, 2), weight=1) # 3 columns for desktop
        
        self.cards = []
        self.populate()

    def populate(self):
        # Clear existing
        for widget in self.winfo_children():
            widget.destroy()
        
        if not self.apps:
            # Empty State
            lbl = ctk.CTkLabel(
                self, 
                text="No apps found in this directory.", 
                font=("Roboto", 16),
                text_color="#94A3B8"
            )
            lbl.pack(pady=40)
            return

        row = 0
        col = 0
        columns = 3
        
        for app in self.apps:
            card = AppCard(self, app, self.run_callback, self.edit_callback, self.delete_callback)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
            
            col += 1
            if col >= columns:
                col = 0
                row += 1
