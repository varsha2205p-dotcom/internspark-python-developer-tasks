import os
import shutil
import logging

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(
    filename="operations.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# File Categories
# -------------------------------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Python": [".py"],
    "Compressed": [".zip", ".rar", ".7z"],
}


def get_category(extension):
    """Return the category of a file based on its extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category

    return "Others"


def organize_files(folder_path):
    """Organize files into category folders."""

    try:
        if not os.path.exists(folder_path):
            print("Error: Folder does not exist.")
            logging.error("Folder does not exist: %s", folder_path)
            return

        if not os.path.isdir(folder_path):
            print("Error: The provided path is not a folder.")
            logging.error("Path is not a folder: %s", folder_path)
            return

        files = os.listdir(folder_path)

        for file_name in files:

            file_path = os.path.join(folder_path, file_name)

            # Skip directories
            if os.path.isdir(file_path):
                continue

            _, extension = os.path.splitext(file_name)

            category = get_category(extension)

            category_folder = os.path.join(folder_path, category)

            # Create category folder if it doesn't exist
            if not os.path.exists(category_folder):
                os.makedirs(category_folder)
                logging.info("Created folder: %s", category_folder)

            destination = os.path.join(category_folder, file_name)

            # Handle duplicate file names
            if os.path.exists(destination):
                base_name, ext = os.path.splitext(file_name)
                counter = 1

                while os.path.exists(destination):
                    new_name = f"{base_name}_{counter}{ext}"
                    destination = os.path.join(category_folder, new_name)
                    counter += 1

            shutil.move(file_path, destination)

            print(f"Moved: {file_name} -> {category}/")
            logging.info(
                "Moved file: %s -> %s",
                file_path,
                destination
            )

        print("\nFile organization completed successfully!")
        logging.info("File organization completed successfully.")

    except PermissionError:
        print("Error: Permission denied.")
        logging.exception("Permission denied while organizing files.")

    except OSError as error:
        print(f"OS Error: {error}")
        logging.exception("OS error occurred.")

    except Exception as error:
        print(f"Unexpected error: {error}")
        logging.exception("Unexpected error occurred.")


def rename_files(folder_path):
    """Rename files by adding a prefix."""

    try:
        if not os.path.isdir(folder_path):
            print("Invalid folder path.")
            logging.error("Invalid folder path: %s", folder_path)
            return

        prefix = input("Enter the prefix for file names: ").strip()

        if not prefix:
            print("Prefix cannot be empty.")
            return

        count = 1

        for file_name in os.listdir(folder_path):

            old_path = os.path.join(folder_path, file_name)

            if os.path.isfile(old_path):
                name, extension = os.path.splitext(file_name)

                new_name = f"{prefix}_{count}{extension}"
                new_path = os.path.join(folder_path, new_name)

                os.rename(old_path, new_path)

                print(f"Renamed: {file_name} -> {new_name}")

                logging.info(
                    "Renamed file: %s -> %s",
                    file_name,
                    new_name
                )

                count += 1

        print("\nRenaming completed successfully!")

    except Exception as error:
        print(f"Error while renaming files: {error}")
        logging.exception("Error during file renaming.")


def main():
    print("=" * 50)
    print("       FILE ORGANIZER AUTOMATION TOOL")
    print("=" * 50)

    folder_path = input(
        "\nEnter the folder path to process: "
    ).strip()

    while True:

        print("\nChoose an operation:")
        print("1. Organize files")
        print("2. Rename files")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            organize_files(folder_path)

        elif choice == "2":
            rename_files(folder_path)

        elif choice == "3":
            print("Thank you for using File Organizer!")
            logging.info("Program exited by user.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
