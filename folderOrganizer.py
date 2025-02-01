import os
import shutil
from typing import Dict, List, Tuple
from extensionMaps import EXTENSION_MAPS


class FolderOrganizer:
    def __init__(self, extension_maps: Dict[str, List[str]] | None = None):
        # Dictionary of file categories and their extensions
        self.extension_maps: Dict[
            str, List[str]] = self.get_default_extension_maps() if extension_maps is None else extension_maps

        # List to track moves for undo functionality
        self.move_histories: List[List[tuple]] = []

    @staticmethod
    def get_default_extension_maps() -> Dict[str, List[str]]:
        return EXTENSION_MAPS.copy()

    def set_extension_maps(self, new_maps: Dict[str, List[str]]) -> None:
        """Replace the current extension maps with new ones."""
        self.extension_maps = new_maps.copy()

    def get_extension_maps(self) -> Dict[str, List[str]]:
        """Get a copy of the current extension maps."""
        return {k: v.copy() for k, v in self.extension_maps.items()}

    def add_extension_category(self, category: str, extensions: List[str]) -> None:
        """Add a new category with its associated file extensions."""
        self.extension_maps[category] = extensions

    def add_extensions_to_category(self, category: str, extensions: List[str]) -> None:
        """Add new extensions to an existing category."""
        if category in self.extension_maps:
            self.extension_maps[category].extend(extensions)
        else:
            self.add_extension_category(category, extensions)

    def remove_category(self, category: str) -> None:
        """Remove a category and its associated extensions."""
        if category in self.extension_maps:
            del self.extension_maps[category]

    def get_category_for_extension(self, file_extension: str) -> str:
        """Determine which category a file extension belongs to."""
        for category, extensions in self.extension_maps.items():
            if file_extension.lower() in extensions:
                return category
        return 'Others'  # Default category for unrecognized extensions

    def get_required_folders(self, directory: str) -> set:
        """Determine which category folders are needed based on files present."""
        required_folders = set()

        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                file_extension = os.path.splitext(filename)[1].lower()
                folder_found = False

                # Check if the file belongs to any category
                for category, extensions in self.extension_maps.items():
                    if file_extension in extensions:
                        required_folders.add(category)
                        folder_found = True
                        break

                # If no category found, file will go to Others
                if not folder_found:
                    required_folders.add('Others')

        return required_folders

    def create_category_folders(self, directory: str) -> None:
        """Create only the necessary category folders based on files present."""
        required_folders = self.get_required_folders(directory)

        for folder in required_folders:
            folder_path = os.path.join(directory, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def organize_folder(self, directory: str) -> None:
        """Organize files in the specified directory into categories."""
        # Convert directory to absolute path
        directory = os.path.abspath(directory)

        # Create category folders
        self.create_category_folders(directory)

        # Create a new move history for this operation
        current_move_history = []

        # Iterate through all files in the directory
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            # Skip if it's a directory or hidden file
            if os.path.isdir(item_path) or item.startswith('.'):
                continue

            # Get file extension and category
            file_extension = os.path.splitext(item)[1].lower()
            category = self.get_category_for_extension(file_extension)

            # Create destination path
            destination_folder = os.path.join(directory, category)
            destination_path = os.path.join(destination_folder, item)

            # Move file to appropriate category folder and track the move
            try:
                shutil.move(item_path, destination_path)
                # Record the move in the current move history
                current_move_history.append((destination_path, item_path))
                print(f"Moved '{item}' to {category} folder")
            except Exception as e:
                print(f"Error moving '{item}': {str(e)}")

        # Append to total history moves
        self.create_move_history(current_move_history)

    def undo_last_operation(self) -> None:
        """Undo the last organization operation by moving files back to their original locations."""
        if not self.move_histories:
            print("No moves to undo.")
            return

        # Get the last move history
        last_move_history = self.move_histories.pop()

        for destination_path, original_path in reversed(last_move_history):
            try:
                shutil.move(destination_path, original_path)
                print(f"Moved '{os.path.basename(destination_path)}' back to original location")
            except Exception as e:
                print(f"Error undoing move for '{os.path.basename(destination_path)}': {str(e)}")

    def create_move_history(self, new_history_move: List[Tuple[str, str]]) -> None:
        """Appends a new history move to the move histories list, maintaining a maximum of 15 entries."""
        if len(self.move_histories) >= 15:
            del self.move_histories[0]
        self.move_histories.append(new_history_move)

    def get_move_history(self, index: int = -1) -> list:
        """Get the move history for a specific operation. Defaults to the last operation."""
        if not self.move_histories:
            return []
        return self.move_histories[index]

    def clear_move_histories(self) -> None:
        """Clear all move histories."""
        self.move_histories.clear()


def main():
    # Create organizer instance
    organizer = FolderOrganizer()

    # Example of adding new category and extensions
    # organizer.add_extension_category('eBooks', ['.epub', '.mobi', '.azw'])
    # organizer.add_extensions_to_category('Documents', ['.rtf', '.odt'])

    # Get directory path from user
    while True:
        directory = input("Enter the directory path to organize: ").strip()
        if os.path.exists(directory):
            break
        print("Invalid directory path. Please try again.")

    # Organize the folder
    organizer.organize_folder(directory)
    print("Organization complete!")

    # Option to undo
    undo_choice = input("Do you want to undo the organization? (yes/no): ").strip().lower()
    if undo_choice == 'yes':
        organizer.undo_last_operation()


if __name__ == "__main__":
    main()
