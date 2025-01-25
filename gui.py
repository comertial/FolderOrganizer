import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import builtins
import shutil
from folderOrganizer import FolderOrganizer

class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x600")

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

    def toggle_theme(self):
        if self.is_dark_theme:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        self.is_dark_theme = not self.is_dark_theme

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
