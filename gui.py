import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
from typing import Union
import sys
import os
import builtins
import shutil
import json
from folderOrganizer import FolderOrganizer


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        # Running in development mode, use the current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class CategoryManager:
    def __init__(self, root, organizer: FolderOrganizer, status_callback):
        self.root = root
        self.organizer = organizer
        self.status_callback = status_callback
        self.current_category = None
        self.current_extension = None

        self.setup_ui()
        self.refresh_categories()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Categories Section
        ctk.CTkLabel(main_frame, text="Categories:").grid(row=0, column=0, sticky="w")

        # Category Listbox
        self.category_list = ctk.CTkScrollableFrame(main_frame, width=200, height=150)
        self.category_list.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Category Entry
        self.category_entry = ctk.CTkEntry(main_frame, width=200)
        self.category_entry.grid(row=2, column=0, padx=5, pady=5)

        # Category Buttons
        category_btn_frame = ctk.CTkFrame(main_frame)
        category_btn_frame.grid(row=3, column=0, pady=5)
        ctk.CTkButton(category_btn_frame, text="Add", width=95, command=self.add_category).grid(row=0, column=0, padx=2)
        ctk.CTkButton(category_btn_frame, text="Remove", width=95, command=self.remove_category).grid(row=0, column=1,
                                                                                                      padx=2)

        # Extensions Section
        ctk.CTkLabel(main_frame, text="Extensions:").grid(row=0, column=1, sticky="w")

        # Extensions Listbox
        self.extensions_list = ctk.CTkScrollableFrame(main_frame, width=200, height=150)
        self.extensions_list.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # Extension Entry
        self.extension_entry = ctk.CTkEntry(main_frame, width=200)
        self.extension_entry.grid(row=2, column=1, padx=5, pady=5)

        # Extension Buttons
        extension_btn_frame = ctk.CTkFrame(main_frame)
        extension_btn_frame.grid(row=3, column=1, pady=5)
        ctk.CTkButton(extension_btn_frame, text="Add", width=95, command=self.add_extension).grid(row=0, column=0,
                                                                                                  padx=2)
        ctk.CTkButton(extension_btn_frame, text="Remove", width=95, command=self.remove_extension).grid(row=0, column=1,
                                                                                                        padx=2)

        # Configure grid weights
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Bind selection events
        self.bind_selection_events()

    def refresh_ui(self):
        """Refresh all UI elements with current theme settings."""
        # Update base frame colors
        self.root.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])

        # Refresh all elements
        self.refresh_categories()
        self.refresh_extensions()

        # Update entry fields
        self.category_entry.configure(text_color=ctk.ThemeManager.theme["CTkEntry"]["text_color"])
        self.extension_entry.configure(text_color=ctk.ThemeManager.theme["CTkEntry"]["text_color"])

    def bind_selection_events(self):
        # Bind category selection
        for child in self.category_list.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.bind("<Button-1>", lambda e, btn=child: self.select_category(btn.cget("text")))

        # Bind extension selection
        for child in self.extensions_list.winfo_children():
            if isinstance(child, ctk.CTkLabel):
                child.bind("<Button-1>", lambda e, lbl=child: self.select_extension(lbl.cget("text")))

    def refresh_categories(self):
        """Refresh the list of categories."""
        # Clear existing widgets
        for widget in self.category_list.winfo_children():
            widget.destroy()

        # Add new category buttons with theme-adaptive colors
        for category in self.organizer.get_extension_maps():
            btn = ctk.CTkButton(
                self.category_list,
                text=category,
                anchor="w",
                corner_radius=5,
                fg_color="transparent",
                text_color=("gray10", "gray90")  # Dark in light theme, light in dark theme
            )
            btn.pack(fill="x", pady=2)
            btn.bind("<Button-1>", lambda e, c=category: self.select_category(c))

        self.refresh_extensions()

    def refresh_extensions(self):
        """Refresh the list of extensions for the selected category."""
        for widget in self.extensions_list.winfo_children():
            widget.destroy()

        if self.current_category:
            extensions = self.organizer.get_extension_maps().get(self.current_category, [])
            for ext in extensions:
                btn = ctk.CTkButton(
                    self.extensions_list,
                    text=ext,
                    anchor="w",
                    corner_radius=5,
                    fg_color="transparent",
                    text_color=("gray10", "gray90")
                )
                btn.pack(fill="x", pady=2)

                # Use a helper function to capture the extension
                def make_handler(extension):
                    return lambda e: self.select_extension(extension)

                btn.bind("<Button-1>", make_handler(ext))

        self.bind_selection_events()

    def select_category(self, category: str):
        """Select a category and show its extensions."""
        self.current_category = category
        self.category_entry.delete(0, "end")
        self.category_entry.insert(0, category)
        self.refresh_extensions()

    def select_extension(self, extension: str):
        """Select an extension."""
        self.current_extension = extension
        self.extension_entry.delete(0, "end")
        self.extension_entry.insert(0, extension)

    def add_category(self):
        """Add a new category."""
        new_category = self.category_entry.get().strip()
        if not new_category:
            messagebox.showerror("Error", "Please enter a category name!")
            return

        if new_category in self.organizer.get_extension_maps():
            messagebox.showerror("Error", "Category already exists!")
            return

        self.organizer.add_extension_category(new_category, [])
        self.category_entry.delete(0, "end")
        self.refresh_categories()
        self.status_callback(f"Added category: {new_category}")

    def remove_category(self):
        """Remove the selected category."""
        category_to_remove = self.category_entry.get().strip()
        if not category_to_remove:
            messagebox.showerror("Error", "No category selected!")
            return

        self.organizer.remove_category(category_to_remove)
        self.category_entry.delete(0, "end")
        self.current_category = None
        self.refresh_categories()
        self.status_callback(f"Removed category: {category_to_remove}")

    def add_extension(self):
        """Add an extension to the current category with validation."""
        if not self.current_category:
            messagebox.showerror("Error", "No category selected!")
            return

        new_ext = self.extension_entry.get().strip().lower()
        if not new_ext.startswith('.'):
            new_ext = '.' + new_ext

        if not new_ext:
            messagebox.showerror("Error", "Please enter an extension!")
            return

        # Check for duplicate in current category
        current_extensions = self.organizer.get_extension_maps().get(self.current_category, [])
        if new_ext in current_extensions:
            messagebox.showerror("Error", f"Extension {new_ext} already exists in this category!")
            return

        # Check for existence in other categories
        conflicting_categories = []
        for category, extensions in self.organizer.get_extension_maps().items():
            if category != self.current_category and new_ext in extensions:
                conflicting_categories.append(category)

        if conflicting_categories:
            conflict_list = "\n- ".join(conflicting_categories)
            response = messagebox.askyesno(
                "Conflict Detected",
                f"Extension {new_ext} already exists in:\n- {conflict_list}\n\nAdd anyway?"
            )
            if not response:
                return

        # Add the extension if all checks pass
        self.organizer.add_extensions_to_category(self.current_category, [new_ext])
        self.extension_entry.delete(0, "end")
        self.refresh_extensions()
        self.status_callback(f"Added extension {new_ext} to {self.current_category}")

    def remove_extension(self):
        """Remove the selected extension."""
        if not self.current_category:
            messagebox.showerror("Error", "No category selected!")
            return

        ext_to_remove = self.extension_entry.get().strip().lower()
        if not ext_to_remove.startswith('.'):
            ext_to_remove = '.' + ext_to_remove

        current_extensions = self.organizer.get_extension_maps().get(self.current_category, [])
        if ext_to_remove in current_extensions:
            current_extensions.remove(ext_to_remove)
            self.organizer.add_extension_category(self.current_category, current_extensions)
            self.extension_entry.delete(0, "end")
            self.refresh_extensions()
            self.status_callback(f"Removed extension {ext_to_remove} from {self.current_category}")
        else:
            messagebox.showerror("Error", "Extension not found in category!")

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x600")

        # Set the window icon
        icon_path = resource_path("assets/icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print("Icon file not found. Ensure the path is correct.")

        # Theme state and appearance mode
        self.is_dark_theme = True
        ctk.set_appearance_mode("dark")  # Default to dark theme

        # Create the organizer instance
        self.organizer = FolderOrganizer()

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Set up the GUI elements
        self.setup_gui()
        self.management_window = None  # Track category management window

    def setup_gui(self):
        # Theme Toggle Button
        self.theme_button = ctk.CTkButton(
            self.main_frame,
            text="Toggle Theme",
            command=self.toggle_theme,
            corner_radius=5
        )
        self.theme_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Directory Selection
        ctk.CTkLabel(self.main_frame, text="Select Directory to Organize:",
                     font=('Helvetica', 12)).grid(row=0, column=0, pady=10, sticky="w")

        self.directory_var = ctk.StringVar()
        self.directory_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.directory_var,
            width=400,
            corner_radius=5
        )
        self.directory_entry.grid(row=1, column=0, padx=5, pady=5)

        ctk.CTkButton(self.main_frame, text="Browse",
                      command=self.browse_directory, corner_radius=5).grid(row=1, column=1, padx=5)

        # Organize and Undo Buttons
        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ctk.CTkButton(button_frame, text="Organize Files",
                      command=self.organize_files, corner_radius=5).grid(row=0, column=0, padx=5)

        ctk.CTkButton(button_frame, text="Undo",
                      command=self.undo_organization, corner_radius=5).grid(row=0, column=1, padx=5)

        # Status Text
        self.status_text = ctk.CTkTextbox(self.main_frame, height=300, width=700, corner_radius=5)
        self.status_text.grid(row=3, column=0, columnspan=2, pady=10)

        # Progress Bar
        self.progress_var = ctk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            self.main_frame,
            variable=self.progress_var,
            orientation="horizontal",
            mode="determinate",
            width=700
        )
        self.progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

        control_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        control_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ctk.CTkButton(control_frame, text="Manage Categories",
                      command=self.open_management_window, corner_radius=5).grid(row=0, column=0, padx=5)
        ctk.CTkButton(control_frame, text="Save Maps",
                      command=self.save_maps, corner_radius=5).grid(row=0, column=1, padx=5)
        ctk.CTkButton(control_frame, text="Load Maps",
                      command=self.load_maps, corner_radius=5).grid(row=0, column=2, padx=5)

    def open_management_window(self):
        """Open the category management window."""
        if self.management_window and self.management_window.winfo_exists():
            self.management_window.lift()
            self.management_window.focus_force()
            return

        self.management_window = ctk.CTkToplevel(self.root)
        self.management_window.title("Manage Categories")
        self.management_window.geometry("600x500")

        # Force window to stay on top of main window
        self.management_window.transient(self.root)
        self.management_window.attributes('-topmost', True)  # Temporarily force to front
        self.management_window.after(100, lambda: self.management_window.attributes('-topmost', False))

        # Create category manager and focus
        self.management_window.category_manager = CategoryManager(
            self.management_window, self.organizer, self.update_status
        )

        # Bring to front and focus
        self.management_window.lift()
        self.management_window.focus_force()

    def save_maps(self):
        """Save current extension maps to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w') as f:
                json.dump(self.organizer.get_extension_maps(), f, indent=4)
            self.update_status(f"Extension maps saved to {file_path}")
            messagebox.showinfo("Success", "Extension maps saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save maps: {str(e)}")

    def load_maps(self):
        """Load extension maps from a JSON file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                new_maps = json.load(f)
            self.organizer.set_extension_maps(new_maps)
            self.update_status(f"Extension maps loaded from {file_path}")
            messagebox.showinfo("Success", "Extension maps loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load maps: {str(e)}")

    def toggle_theme(self):
        if self.is_dark_theme:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        self.is_dark_theme = not self.is_dark_theme

        # Force refresh all UI components
        if self.management_window and self.management_window.winfo_exists():
            self.management_window.category_manager.refresh_ui()

        # Update main window elements
        self.main_frame.configure(fg_color=ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.status_text.configure(text_color=ctk.ThemeManager.theme["CTkTextbox"]["text_color"])

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)

    def update_status(self, message):
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.root.update()

    class GUIProgress:
        def __init__(self, gui, total_files):
            self.gui = gui
            self.counter = 0
            self.total = total_files
            self.original_move = shutil.move

        def custom_print(self, message):
            self.gui.update_status(message)

        def custom_move(self, src, dst):
            self.original_move(src, dst)
            self.counter += 1
            progress = (self.counter / self.total)
            self.gui.progress_var.set(progress)
            self.gui.root.update()

    def setup_progress_handling(self, total_files: int) -> tuple:
        progress_handler = self.GUIProgress(self, total_files)
        original_print = builtins.print
        original_move = shutil.move
        builtins.print = progress_handler.custom_print
        shutil.move = progress_handler.custom_move
        return original_print, original_move

    def validate_directory(self) -> bool:
        directory = self.directory_var.get()
        if not directory:
            messagebox.showerror("Error", "Please select a directory first!")
            return False
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Selected directory does not exist!")
            return False
        return True

    def get_file_list(self, directory: str) -> list:
        files = [f for f in os.listdir(directory)
                 if os.path.isfile(os.path.join(directory, f))
                 and not f.startswith('.')]
        if not files:
            self.update_status("No files to organize!")
        return files

    def organize_files(self):
        if not self.validate_directory():
            return

        directory = self.directory_var.get()
        files = self.get_file_list(directory)

        if not files:
            return

        self.progress_var.set(0)
        self.update_status("Starting organization...")

        try:
            # Setup progress handling
            original_print, original_move = self.setup_progress_handling(len(files))
            self.organizer.organize_folder(directory)
            self.update_status("\nOrganization complete!")

            # Restore original functions
            builtins.print = original_print
            shutil.move = original_move

            messagebox.showinfo("Success", "Files have been organized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_var.set(0)

    def undo_organization(self):
        self.update_status("Starting undo process...")

        try:
            # Setup progress handling
            undo_files = self.organizer.get_move_history()
            original_print, original_move = self.setup_progress_handling(len(undo_files))
            self.organizer.undo_last_operation()
            self.update_status("\nUndo process complete!")

            # Restore original functions
            builtins.print = original_print
            shutil.move = original_move

            if len(undo_files) > 0:
                messagebox.showinfo("Success", "Files have been moved back to their original locations!")
            else:
                messagebox.showwarning("Warning", "Undo operation did not move any file!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during undo: {str(e)}")

def main():
    root = ctk.CTk()
    app = FileOrganizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
