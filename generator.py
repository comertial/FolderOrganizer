import os
import random
from datetime import datetime
import string
from typing import Dict, List
from extensionMaps import EXTENSION_MAPS


class TestFileGenerator:
    def __init__(self, extension_maps: Dict[str, List[str]] | None = None):
        # Dictionary of file categories and their extensions
        self.extension_maps: Dict[
            str, List[str]] = self.get_default_extension_maps() if extension_maps is None else extension_maps

    @staticmethod
    def get_default_extension_maps() -> Dict[str, List[str]]:
        return EXTENSION_MAPS.copy()

    @staticmethod
    def generate_random_string(length=8):
        """Generate a random string for file names."""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def create_empty_file(self, filepath):
        """Create an empty file with some random content."""
        try:
            with open(filepath, 'w') as f:
                # Write some dummy content
                f.write(f"This is a test file created at {datetime.now()}\n")
                f.write(f"Random content: {self.generate_random_string(50)}")
        except Exception as e:
            print(f"Error creating file {filepath}: {str(e)}")

    def generate_test_files(self, directory: str, files_per_category: int = 3):
        """
        Generate test files in the specified directory.

        Args:
            directory (str): The directory where files should be created
            files_per_category (int): Number of files to create for each extension
        """
        # Create directory if it doesn't exist
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Counter for total files created
        total_files = 0

        # Create files for each category and extension
        for category, extensions in self.extension_maps.items():
            print(f"\nCreating {category} files...")
            for ext in extensions:
                for i in range(files_per_category):
                    filename = f"{self.generate_random_string()}_{i}{ext}"
                    filepath = os.path.join(directory, filename)

                    try:
                        self.create_empty_file(filepath)
                        print(f"Created: {filename}")
                        total_files += 1
                    except Exception as e:
                        print(f"Error creating {filename}: {str(e)}")

        print(f"\nTotal files created: {total_files}")


def main():
    generator = TestFileGenerator()

    # Get directory path from user
    while True:
        directory = input("Enter the directory path where test files should be created: ").strip()
        if os.path.exists(directory) or input(
                f"Directory '{directory}' doesn't exist. Create it? (y/n): ").lower() == 'y':
            break
        print("Please enter a valid directory path.")

    # Get number of files per category
    while True:
        try:
            files_per_category = int(input("Enter number of files to create per extension (default is 3): ") or 3)
            if files_per_category > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    # Generate the test files
    generator.generate_test_files(directory, files_per_category)


if __name__ == "__main__":
    main()
