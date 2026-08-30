import argparse
import json
import shutil
from pathlib import Path

# Register the file's history in a JSON file
HISTORY_FILE = "organize_history.json"

# Extension mapping for file categories
EXTENSION_MAP = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Installers": [".exe", ".msi", ".deb", ".apk"],
    "Code": [".py", ".json", ".html", ".css", ".js", ".kt", 
             ".java", ".c", ".cpp", ".cs", ".rb", ".php",
             ".sce",".sci", ".ps1",".sh",".bat"]
}

# Function to get the category of a file based on its extension
def get_category(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if not ext:
        return "Others"

    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
            
    return "Others"

# Function to resolve filename collisions
def resolve_collision(target_path: Path) -> Path:
    # If the file already exists in the destination, generate: 
    # name(1).ext, name(2).ext, etc.
    if not target_path.exists():
        return target_path

    parent_dir = target_path.parent
    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1

    # Mientras el archivo exista en destino, probamos con el siguiente índice
    new_path = parent_dir / f"{stem}({counter}){suffix}"
    while new_path.exists():
        counter += 1
        new_path = parent_dir / f"{stem}({counter}){suffix}"

    return new_path

def inspect_and_classify(target_dir: Path):
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"[Error] The path '{target_dir}' is not valid.")
        return

    print(f"Classifying files in: {target_dir.resolve()}\n")

    history = []
    # Get the absolute path of the current script to avoid moving it
    current_script = Path(__file__).resolve()
    
    for item in target_dir.iterdir():
        # Ignore directories, hidden files, the current script, and the log file
        if (
            item.is_dir()
            or item.name.startswith(".")
            or item.resolve() == current_script
            or item.name == HISTORY_FILE
        ):
            continue
        
        category = get_category(item)
        dest_folder = target_dir / category
        dest_folder.mkdir(exist_ok=True)
        
        dest_path = dest_folder / item.name
        
        # Moving the file in a secure way:
                
        # 1. Resolve collision, so we don't overwrite existing files
        final_dest = resolve_collision(dest_path)

        # 2. Register the original and new paths in the history log
        history.append({
            "original_path": str(item.resolve()),
            "current_path": str(final_dest.resolve())
        })

        # 3. Move the file to the destination folder
        shutil.move(str(item), str(final_dest))
        print(f"Moved: {item.name} -> {category}/{final_dest.name}")

    # Save the operation log in a JSON file within the same folder
    if history:
        log_path = target_dir / HISTORY_FILE
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        print(f"\nOperation logged in: {log_path.name}")
    else:
        print("\nNo files found to organize.")

# Function to undo the organization of files based on the history log
def undo_organization(target_dir: Path):
    log_path = target_dir / HISTORY_FILE
    if not log_path.exists():
        print(f"[Error] No history file found in '{target_dir}'. Nothing to undo.")
        return

    with open(log_path, "r", encoding="utf-8") as f:
        history = json.load(f)

    print(f"Undoing organization in: {target_dir.resolve()}\n")
    restored_count = 0

    for entry in history:
        current_path = Path(entry["current_path"])
        original_path = Path(entry["original_path"])

        if current_path.exists():
            # return the file to its original location, resolving any collisions
            dest_path = resolve_collision(original_path)
            shutil.move(str(current_path), str(dest_path))
            print(f"Restored: {current_path.name} -> {dest_path.name}")
            restored_count += 1

    # clean up empty folders created previously
    for category in EXTENSION_MAP.keys():
        folder = target_dir / category
        if folder.exists() and folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()

    # delete "Others" folder if it exists and is empty
    others_folder = target_dir / "Others"
    if others_folder.exists() and others_folder.is_dir() and not any(others_folder.iterdir()):
        others_folder.rmdir()

    # delete the history log after undoing
    log_path.unlink()
    print(f"\nUndo completed: {restored_count} files restored. History file removed.")


def delete_history(target_dir: Path):
    log_path = target_dir / HISTORY_FILE
    if not log_path.exists():
        print(f"[Warning] No history file found in '{target_dir}'.")
        return

    print("=" * 60)
    print("WARNING!")
    print("If you delete the history file, you will NOT be able to")
    print("automatically undo the previous organization.")
    print("=" * 60)
    
    confirm = input("Are you sure you want to delete it? (y/n): ").strip().lower()
    
    if confirm in ("y", "yes"):
        log_path.unlink()
        print(f"\n[OK] History log deleted: {log_path.name}")
    else:
        print("\nOperation cancelled. History log was kept intact.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files by category, undo operations, or manage history log."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target directory (default: current directory)"
    )
    parser.add_argument(
        "-u", "--undo",
        action="store_true",
        help="Undo the last organization using the history log"
    )
    parser.add_argument(
        "--clear-history",
        action="store_true",
        help="Delete the history log file permanently"
    )

    args = parser.parse_args()
    target_folder = Path(args.path).resolve()
    log_path = target_folder / HISTORY_FILE

    # CLI explicit mode
    if args.undo:
        undo_organization(target_folder)
    elif args.clear_history:
        delete_history(target_folder)
    # Interactive / Double-click mode when history exists
    elif log_path.exists():
        print(f"Target: {target_folder.name}")
        print("Previous organization history found.\n")
        print("1. Organize new files")
        print("2. Undo last organization")
        print("3. Delete history log (You'll not be able to undo changes)")
        
        choice = input("\nChoose an option (1, 2, or 3): ").strip()
        print()
        
        if choice == "2":
            undo_organization(target_folder)
        elif choice == "3":
            delete_history(target_folder)
        else:
            inspect_and_classify(target_folder)
            
        input("\nPress Enter to exit...")
    # Default first run
    else:
        inspect_and_classify(target_folder)
        input("\nPress Enter to exit...")