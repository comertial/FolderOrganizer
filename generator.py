import os
import random
from datetime import datetime
import string
from typing import Dict, List


class TestFileGenerator:
    def __init__(self):
        # Dictionary of file categories and their extensions
        self.file_types: Dict[str, List[str]] = {
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

    def generate_random_string(self, length=8):
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
        for category, extensions in self.file_types.items():
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
