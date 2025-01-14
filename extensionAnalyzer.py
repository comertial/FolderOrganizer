from typing import Dict, List, Set
from collections import defaultdict
from pprint import pprint


class ExtensionAnalyzer:
    def __init__(self):
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
