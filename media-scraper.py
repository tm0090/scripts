import os
import shutil
import mimetypes
from pathlib import Path

def get_unique_filename(dest_folder: Path, filename: str) -> Path:
    """Ensures duplicate filenames are renamed (e.g., photo_1.jpg) to avoid overwriting."""
    target_path = dest_folder / filename
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1

    while True:
        new_path = dest_folder / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

def collect_media():
    print("=== Media File Consolidator ===")
    
    # Prompt for paths
    source_input = input("Enter the parent source folder path: ").strip()
    dest_input = input("Enter the destination folder path: ").strip()

    source_dir = Path(os.path.expanduser(source_input)).resolve()
    dest_dir = Path(os.path.expanduser(dest_input)).resolve()

    # Validation
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    if source_dir == dest_dir or dest_dir in source_dir.parents:
        print("Error: Destination folder cannot be inside the source folder.")
        return

    dest_dir.mkdir(parents=True, exist_ok=True)

    # Media extension fallback list
    media_extensions = {
        # Images
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", 
        ".heic", ".raw", ".cr2", ".nef", ".arw", ".dng",
        # Videos
        ".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm", ".m4v", ".3gp"
    }

    mimetypes.init()
    moved_count = 0
    skipped_count = 0

    print("\nScanning subfolders for images and videos...\n")

    # Walk through all directories and subdirectories
    for root, _, files in os.walk(source_dir):
        for file_name in files:
            file_path = Path(root) / file_name

            # Skip files already in destination if scanning in overlapping paths
            if dest_dir in file_path.parents:
                continue

            # Check if file is image or video via MIME type or extension fallback
            mime_type, _ = mimetypes.guess_type(file_path)
            is_media = False

            if mime_type and (mime_type.startswith("image/") or mime_type.startswith("video/")):
                is_media = True
            elif file_path.suffix.lower() in media_extensions:
                is_media = True

            if is_media:
                target_path = get_unique_filename(dest_dir, file_name)
                try:
                    shutil.move(str(file_path), str(target_path))
                    print(f"Moved: {file_path.name} -> {target_path.name}")
                    moved_count += 1
                except Exception as e:
                    print(f"Failed to move {file_path.name}: {e}")
                    skipped_count += 1

    print("-" * 50)
    print(f"Finished! Successfully moved {moved_count} media files to:")
    print(f"{dest_dir}")
    if skipped_count > 0:
        print(f"Skipped/Errors: {skipped_count} files")

if __name__ == "__main__":
    collect_media()