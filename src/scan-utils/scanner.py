from src.dl_cli.schemas import RootFileSchema
import os
from pathlib import Path
import fnmatch
from src.dl_cli.root_manager import RootDbManager as root_db

# These directories can contain 10k-100k+ files each
IGNORE_DIRS = [
    # Version control
    '.git',
    '.svn',
    '.hg',

    # Package managers & dependencies
    'node_modules',
    'bower_components',
    'vendor',
    'packages',

    # Python environments
    '.venv',
    'venv',
    '.virtualenv',
    '__pycache__',
    '.tox',
    '.pytest_cache',
    'site-packages',

    # Build outputs
    'dist',
    'build',
    'target',
    'out',
    'bin',
    'obj',

    # IDE/Editor
    '.vscode',
    '.idea',
    '.vs',

    # OS/System
    'AppData',
    'Application Data',
    'Local Settings',
    'Temp',
    'tmp',
    '$RECYCLE.BIN',
    'System Volume Information',

    # Large media/cache dirs
    '.cache',
    'cache',
    'Cache',
    'Caches',
    'Downloads',  # Often huge
    'Music',
    'Videos',
    'Pictures',
    'Documents/My Music',
    'Documents/My Videos',
    'Documents/My Pictures',
]

# File extensions to completely skip
IGNORE_EXTENSIONS = {
    # Media
    '.mp4', '.avi', '.mkv', '.mov', '.mp3', '.wav', '.flac', '.m4a',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico',
    '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',

    # Archives
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',

    # Executables
    '.exe', '.msi', '.dll', '.so', '.dylib',

    # Large data
    '.log', '.bak', '.tmp', '.temp', '.cache',
}

# Target extensions (what you want)
TARGET_EXTENSIONS = {
    # Code
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h',
    '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
    '.sh', '.bash', '.ps1', '.cmd', '.bat',

    # Config/Data
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    '.xml', '.csv', '.tsv', '.sql',

    # Database
    '.db', '.sqlite', '.sqlite3', '.mdb',

    # Web
    '.html', '.htm', '.css', '.scss', '.sass', '.less',

    # Documentation
    '.md', '.rst', '.txt', '.readme',

    # Docker/DevOps
    'Dockerfile', '.dockerignore', '.env', '.gitignore', '.gitattributes',
    'docker-compose.yml', 'docker-compose.yaml',

    # No extension files (common in dev)
    '',  # Will handle specially
}

# Include these even if they're in typically ignored locations
SPECIAL_INCLUDES = [
    '**/.dev/versions/*',  # Your build tools
    '**/.github/workflows/*',  # GitHub Actions
    '**/.vscode/settings.json',  # VS Code settings
    '**/.env*',  # Environment files
    '**/docker-compose*.yml',
    '**/Dockerfile*',
]


def should_ignore_dir(dir_name, ignore_dirs):
    return any(fnmatch.fnmatch(dir_name.lower(), pattern.lower())
               for pattern in ignore_dirs)


def should_include_file(file_path, target_extensions, ignore_extensions):
    path_obj = Path(file_path)

    # Special handling for extensionless files
    if not path_obj.suffix:
        # Include common extensionless config files
        if path_obj.name.lower() in {
            'dockerfile', 'makefile', 'rakefile', 'gemfile', 'procfile',
            '.env', '.gitignore', '.dockerignore', '.gitattributes'
        }:
            return True
        # Include files in .dev/versions/ regardless of extension
        if '.dev' in path_obj.parts and 'versions' in path_obj.parts:
            return True
        return False

    ext = path_obj.suffix.lower()

    # Skip ignored extensions
    if ext in ignore_extensions:
        return False

    # Include target extensions
    return ext in target_extensions


def scan_user_directory(
        user_path,
        use_special_includes=False,
        extra_includes=None
):
    files = []

    for root, dirs, filenames in os.walk(user_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if not should_ignore_dir(d, IGNORE_DIRS)]

        # Handle special includes
        if extra_includes:
            for pattern in extra_includes:
                if fnmatch.fnmatch(root, pattern):
                    # If the root matches an extra include, don't skip it
                    break
            else:
                # If no extra include matched, skip this directory
                continue

        # Handle special includes for .dev/versions
        if use_special_includes:
            for pattern in SPECIAL_INCLUDES:
                if fnmatch.fnmatch(root, pattern):
                    # If the root matches a special include, don't skip it
                    break
            else:
                # If no special include matched, skip this directory
                continue

        # Collect files
        for filename in filenames:
            filepath = os.path.join(root, filename)

            # Check if the file should be included
            if should_include_file(
                filepath,
                TARGET_EXTENSIONS,
                IGNORE_EXTENSIONS
            ):
                try:
                    stat = os.stat(filepath)
                    # Only include files smaller than 10MB for text files
                    if stat.st_size < 10 * 1024 * 1024:
                        files.append({
                            'path': filepath,
                            'name': filename,
                            'size': stat.st_size,
                            'modified': stat.st_mtime,
                            'extension': Path(filepath).suffix.lower(),
                            'parent': str(Path(filepath).parent),
                        })
                except (OSError, IOError):
                    continue
            root_db.add_files(files)
    return files


def scan_all_roots(
    **kwargs
):
    if 'path' in kwargs:
        raise ValueError(
            "The 'path' argument is not supported for scan_all_roots. Use scan_user_directory instead."
        )

    roots = root_db.list_roots()
    all_files = []

    for root in roots:
        files = scan_user_directory(root.path, **kwargs)
        all_files.extend(files)

    return all_files
