import os
import shutil
from pathlib import Path
from typing import Dict, List


class FolderOrganizer:
    def __init__(self):
        # Dictionary mapping categories to their file extensions
        self.extension_maps: Dict[str, List[str]] = {
            'Documents': [
                # Microsoft Office
                '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                # OpenOffice/LibreOffice
                '.odt', '.ods', '.odp',
                # Text files
                '.txt', '.rtf', '.md', '.csv',
                # PDF and similar
                '.pdf',
                # Other documents
                '.tex', '.pages', '.numbers',
                # Additional formats
                '.wpd', '.wps', '.pub', '.one', '.note', '.xml-doc',
                '.gdoc', '.gsheet', '.gslides', '.pdx', '.latex'
            ],

            'Images': [
                # Common formats
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
                # Raw formats
                '.raw', '.cr2', '.nef', '.arw', '.dng',
                # Vector and design
                '.svg', '.ai', '.eps', '.psd',
                # Other formats
                '.webp', '.ico', '.heic', '.jfif',
                # Additional formats
                '.xcf', '.cdr', '.sketch', '.fig', '.afdesign', '.kra',
                '.pcx', '.pgm', '.ppm', '.xpm', '.hdr', '.exr'
            ],

            'Videos': [
                # Common formats
                '.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv',
                # Other formats
                '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2',
                # Professional formats
                '.vob', '.mxf', '.f4v',
                # Additional formats
                '.rm', '.rmvb', '.m2ts', '.ts', '.asf', '.divx',
                '.ogv', '.dv', '.fcpx', '.kdenlive', '.vpj'
            ],

            'Audio': [
                # Common formats
                '.mp3', '.wav', '.flac', '.m4a', '.aac',
                # Other formats
                '.wma', '.ogg', '.opus', '.mid', '.midi',
                # Professional formats
                '.aif', '.aiff', '.alac', '.dsd', '.dsf',
                # Project files
                '.fpl', '.aup', '.reapeaks', '.sesx',
                # Additional formats
                '.ape', '.mka', '.mpc', '.ac3', '.dts',
                '.amr', '.au', '.ra', '.voc', '.pcm'
            ],

            'Archives': [
                # Common formats
                '.zip', '.rar', '.7z', '.tar', '.gz',
                # Other formats
                '.bz2', '.xz', '.iso', '.tgz', '.zipx',
                '.pkg', '.deb', '.rpm',
                # Additional formats
                '.arc', '.arj', '.cab', '.lzh', '.lha',
                '.z', '.ace', '.uue', '.zoo', '.pea'
            ],

            'Code': [
                # Web development
                '.jsx',
                # Programming languages
                '.py', '.java', '.cpp', '.c', '.cs', '.h', '.hpp', '.swift',
                '.kt', '.rs', '.go', '.rb', '.pl', '.lua',
                # Scripts and config
                '.sh', '.bash', '.ps1', '.yaml', '.yml',
                # IDE and config files
                '.conf', '.config', '.lock', '.env',
                # Additional languages
                '.scala', '.groovy', '.dart', '.elm', '.erl', '.ex',
                '.fs', '.fsx', '.hs', '.lhs', '.ml', '.nim',
                '.r', '.rkt', '.tcl', '.vb'
            ],

            'Databases': [
                '.sql', '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb',
                '.frm', '.myd', '.myi', '.ibd', '.dbf'
            ],

            'Fonts': [
                '.ttf', '.otf', '.woff', '.woff2', '.eot', '.fnt',
                '.fon', '.pfm', '.pfb'
            ],

            'CAD_3D': [
                # CAD files
                '.dwg', '.dxf', '.step', '.stp', '.iges', '.igs',
                # 3D models
                '.stl', '.obj', '.fbx', '.3ds', '.blend', '.max',
                '.maya', '.c4d', '.skp'
            ],

            'Executables': [
                '.exe', '.msi', '.app', '.dmg', '.apk', '.ipa',
                '.bat', '.cmd', '.com', '.gadget'
            ],

            'Game_Files': [
                '.sav', '.save', '.gba', '.nes', '.n64',
                '.gb', '.gbc', '.nds', '.wad'
            ],

            'Virtual_Machines': [
                '.vdi', '.vmdk', '.ova', '.ovf', '.vhd', '.vhdx',
                '.qcow', '.qcow2'
            ],

            'eBooks': [
                '.epub', '.mobi', '.azw', '.azw3', '.kfx', '.fb2',
                '.lit', '.djvu', '.cbr', '.cbz'
            ],

            'Scientific': [
                '.mat', '.nb', '.cdf', '.fits', '.fts',
                '.hdf', '.h5', '.dx', '.mrc'
            ],

            'Shortcuts': [
                '.lnk', '.url', '.webloc', '.desktop'
            ],

            'System': [
                '.sys', '.dll', '.drv', '.tmp', '.bak', '.cache',
                '.log', '.pid', '.reg', '.ini'
            ],

            'Torrent': [
                '.torrent', '.magnet'
            ],

            'Web': [
                '.html', '.htm', '.xhtml', '.php', '.asp', '.aspx',
                '.jsp', '.css', '.js', '.json', '.xml', '.rss',
                '.webmanifest', '.htaccess'
            ],

            'Design': [
                '.indd', '.xd', '.studio', '.graffle',
                '.drawio', '.vsd', '.aep', '.prproj', '.ppj'
            ],

            'Machine_Learning': [
                '.pkl', '.h5py', '.onnx', '.pb', '.pth',
                '.tfrecords', '.model', '.weights', '.ckpt'
            ],

            'GIS_Data': [
                '.shp', '.geojson', '.kml', '.kmz', '.dem',
                '.gdb', '.mxd', '.qgs', '.osm', '.gpx'
            ],

            'Medical_Imaging': [
                '.dcm', '.nii', '.nii.gz', '.mha', '.mhd',
                '.nrrd', '.vtk', '.analyze'
            ],

            'Mobile_Dev': [
                '.aab', '.dex', '.kotlin',
                '.xcodeproj', '.pbxproj', '.plist', '.gradle'
            ],

            'Network': [
                '.pcap', '.pcapng', '.cap', '.netxml', '.cisco',
                '.pkt', '.snoop', '.etl', '.qxp'
            ],

            'Security': [
                '.key', '.csr', '.crt', '.cer', '.der',
                '.p7b', '.p12', '.pfx', '.pem', '.asc'
            ],

            'Firmware': [
                '.bin', '.fw', '.hex', '.rom', '.firmware',
                '.bios', '.img', '.fth'
            ],

            'Data_Exchange': [
                '.wsdl', '.xsd', '.dtd', '.xslt', '.xpath',
                '.soap', '.graphql', '.proto'
            ],

            'Backup': [
                '.bkp', '.bkf', '.fbk', '.gbk',
                '.backup', '.old', '.orig', '.temp'
            ],

            'Research': [
                '.sps', '.por', '.dta', '.rdata',
                '.rds', '.sas7bdat', '.xpt', '.jmp'
            ],

            'Reports': [
                '.rpt', '.jrxml', '.rdl', '.rdlc', '.rpx',
                '.frx', '.rav', '.rdf'
            ],

            'Cryptocurrency': [
                '.wallet', '.dat', '.eth', '.btc', '.nft',
                '.sol', '.aes', '.crypto', '.chain'
            ]
        }

        # List to track moves for undo functionality
        self.move_histories: List[List[tuple]] = []

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
        self.move_histories.append(current_move_history)

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
                # If an error occurs, remove the current move history
                self.move_histories.pop()

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
