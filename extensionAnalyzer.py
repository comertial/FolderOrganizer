from typing import Dict, List
from collections import defaultdict
from extensionMaps import EXTENSION_MAPS


class ExtensionAnalyzer:
    def __init__(self, extension_maps: Dict[str, List[str]] | None = None):
        # Dictionary of file categories and their extensions
        self.extension_maps: Dict[
            str, List[str]] = self.get_default_extension_maps() if extension_maps is None else extension_maps

    @staticmethod
    def get_default_extension_maps() -> Dict[str, List[str]]:
        return EXTENSION_MAPS

    def get_extension_maps(self) -> Dict[str, List[str]]:
        """
        Get the extension maps configured.
        """
        return self.extension_maps

    def find_duplicates(self) -> Dict[str, List[str]]:
        """
        Find all duplicate extensions and their corresponding categories.
        Returns a dictionary where keys are extensions and values are lists of categories.
        Only includes extensions that appear in multiple categories.
        """
        # Dictionary to store extension -> categories mapping
        ext_to_categories = defaultdict(list)

        # Populate the dictionary
        for category, extensions in self.extension_maps.items():
            for ext in extensions:
                ext_to_categories[ext].append(category)

        # Filter to keep only duplicates
        duplicates = {
            ext: categories
            for ext, categories in ext_to_categories.items()
            if len(categories) > 1
        }

        return duplicates

    def get_extension_count(self) -> Dict[str, int]:
        """
        Count how many times each extension appears.
        """
        ext_count = defaultdict(int)
        for extensions in self.extension_maps.values():
            for ext in extensions:
                ext_count[ext] += 1
        return dict(ext_count)

    def get_category_stats(self) -> Dict[str, int]:
        """
        Get the number of extensions in each category.
        """
        return {
            category: len(extensions)
            for category, extensions in self.extension_maps.items()
        }

    def find_extension_categories(self, extension: str) -> List[str]:
        """
        Find all categories that contain a specific extension.
        """
        if not extension.startswith('.'):
            extension = f'.{extension}'

        return [
            category
            for category, extensions in self.extension_maps.items()
            if extension in extensions
        ]


def main():
    # Initiate analyzer
    analyzer = ExtensionAnalyzer()

    while True:
        print("\nExtension Analyzer Menu:")
        print("1. Find all duplicate extensions")
        print("2. Get extension count with multiple occurrences")
        print("3. Get category statistics")
        print("4. Search for specific extension")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            duplicates = analyzer.find_duplicates()
            if duplicates:
                print("\nDuplicate extensions found:")
                print("---------------------------")
                for ext, categories in sorted(duplicates.items()):
                    print(f"\nExtension: {ext}")
                    print(f"Found in categories: {', '.join(categories)}")
            else:
                print("\nNo duplicate extensions found!")

        elif choice == '2':
            counts = analyzer.get_extension_count()
            print("\nExtension counts with multiple occurrences:")
            print("----------------")
            for ext, count in sorted(counts.items()):
                if count > 1:
                    print(f"{ext}: {count} occurrences")

        elif choice == '3':
            stats = analyzer.get_category_stats()
            print("\nCategory statistics:")
            print("------------------")
            for category, count in sorted(stats.items()):
                print(f"{category}: {count} extensions")
            print(f"\nTotal categories: {len(stats)}")
            print(f"Total unique extensions: {len(set(ext for exts in analyzer.get_extension_maps().values() for ext in exts))}")

        elif choice == '4':
            ext = input("\nEnter extension (with or without dot): ").strip()
            categories = analyzer.find_extension_categories(ext)
            if categories:
                print(f"\nExtension '{ext}' found in categories:")
                print("--------------------------------")
                for category in categories:
                    print(f"- {category}")
            else:
                print(f"\nExtension '{ext}' not found in any category.")

        elif choice == '5':
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
