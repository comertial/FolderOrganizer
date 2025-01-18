import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import builtins
import shutil
from folderOrganizer import FolderOrganizer


class FileOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x600")

        # Theme state
        self.is_dark_theme = False

        # Create style object
        self.style = ttk.Style()

        # Create the organizer instance
        self.organizer = FolderOrganizer()

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Set up the GUI elements
        self.setup_gui()

        # Set initial theme
        self.set_light_theme()

    def setup_gui(self):
        # Theme Toggle Button
        self.theme_button = ttk.Button(
            self.main_frame,
            text="Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

        # Directory Selection
        ttk.Label(self.main_frame, text="Select Directory to Organize:",
                  font=('Helvetica', 12)).grid(row=0, column=0, pady=10, sticky=tk.W)

        self.directory_var = tk.StringVar()
        self.directory_entry = ttk.Entry(self.main_frame,
                                         textvariable=self.directory_var,
                                         width=50)
        self.directory_entry.grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(self.main_frame, text="Browse",
                   command=self.browse_directory).grid(row=1, column=1, padx=5)

        # Organize Button and Undo Button (Centered and closer together)
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Organize Files",
                   command=self.organize_files).grid(row=0, column=0, padx=5)

        ttk.Button(button_frame, text="Undo",
                   command=self.undo_organization).grid(row=0, column=1, padx=5)

        # Status Text
        self.status_text = tk.Text(self.main_frame, height=20, width=70)
        self.status_text.grid(row=3, column=0, columnspan=2, pady=10)

        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL,
                                  command=self.status_text.yview)
        scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.status_text['yscrollcommand'] = scrollbar.set

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.main_frame,
                                            variable=self.progress_var,
                                            maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=2,
                               sticky=(tk.W, tk.E), pady=10)

    def set_dark_theme(self):
        self.root.configure(bg='#2d2d2d')
        self.main_frame.configure(style='Dark.TFrame')
        self.status_text.configure(bg='#3d3d3d', fg='white', insertbackground='white')

        # Configure ttk styles for dark theme
        self.style.configure('TFrame', background='#2d2d2d')

        # Button styling with consistent black text in dark theme
        self.style.configure('TButton',
                             background='#808080',  # Light grey background
                             foreground='#000000',  # Black text
                             bordercolor='#666666',  # Border color
                             lightcolor='#666666',
                             darkcolor='#666666',
                             relief='raised')

        self.style.map('TButton',
                       foreground=[('pressed', '#000000'),  # Keep text black
                                   ('active', '#000000')],  # Keep text black
                       background=[('pressed', '#999999'),  # Lighter when pressed
                                   ('active', '#a6a6a6')])  # Lighter on hover

        self.style.configure('TLabel', background='#2d2d2d', foreground='white')
        self.style.configure('TEntry', fieldbackground='#3d3d3d', foreground='white')
        self.style.configure('Horizontal.TProgressbar',
                             background='#007acc',
                             troughcolor='#3d3d3d')

    def set_light_theme(self):
        # Light theme remains the same
        self.root.configure(bg='#f0f0f0')
        self.main_frame.configure(style='Light.TFrame')
        self.status_text.configure(bg='white', fg='black', insertbackground='black')

        self.style.configure('TFrame', background='#f0f0f0')

        self.style.configure('TButton',
                             background='#e0e0e0',
                             foreground='black',
                             bordercolor='#cccccc',
                             lightcolor='#cccccc',
                             darkcolor='#cccccc',
                             relief='raised')

        self.style.map('TButton',
                       foreground=[('pressed', 'black'),
                                   ('active', 'black')],
                       background=[('pressed', '#d0d0d0'),
                                   ('active', '#e8e8e8')])

        self.style.configure('TLabel', background='#f0f0f0', foreground='black')
        self.style.configure('TEntry', fieldbackground='white', foreground='black')
        self.style.configure('Horizontal.TProgressbar',
                             background='#007acc',
                             troughcolor='#e0e0e0')

    def toggle_theme(self):
        if self.is_dark_theme:
            self.set_light_theme()
        else:
            self.set_dark_theme()
        self.is_dark_theme = not self.is_dark_theme

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)

    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()

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
            progress = (self.counter / self.total) * 100
            self.gui.progress_var.set(progress)
            self.gui.root.update()

    def setup_progress_handling(self, total_files: int) -> tuple:
        progress_handler = self.GUIProgress(self, total_files)
        original_print = builtins.print
        original_move = shutil.move
        builtins.print = progress_handler.custom_print
        shutil.move = progress_handler.custom_move
        return original_print, original_move

    def restore_functions(self, original_print, original_move):
        builtins.print = original_print
        shutil.move = original_move

    def organize_files(self):
        if not self.validate_directory():
            return

        try:
            directory = self.directory_var.get()
            self.status_text.delete(1.0, tk.END)
            self.update_status(f"Starting organization of: {directory}")

            files = self.get_file_list(directory)
            if not files:
                return

            original_print, original_move = self.setup_progress_handling(len(files))

            try:
                self.organizer.organize_folder(directory)
            finally:
                self.restore_functions(original_print, original_move)

            self.update_status("\nOrganization complete!")
            messagebox.showinfo("Success", "Files have been organized!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def undo_organization(self):
        try:
            self.status_text.delete(1.0, tk.END)
            self.update_status(f"Starting undo process")

            undo_files = self.organizer.get_move_history()

            # Override print and shutil.move for progress handling
            original_print, original_move = self.setup_progress_handling(len(undo_files))

            try:
                # Call the undo method from the FolderOrganizer class
                self.organizer.undo_last_operation()
            finally:
                # Restore the original print and shutil.move functions
                self.restore_functions(original_print, original_move)

            self.update_status("\nUndo process complete!")
            if len(undo_files) > 0:
                messagebox.showinfo("Success", "Files have been moved back to their original locations!")
            else:
                messagebox.showwarning("Warning", "Undo operation did not move any file!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during undo: {str(e)}")


def main():
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
