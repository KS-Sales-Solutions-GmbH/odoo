import os
import polib
from tqdm import tqdm

# Define the path to the large .po file
LARGE_PO_FILE = "./translate2.po"
SEARCH_DIR = "./"  # The directory to search for de.po files


def load_large_po_translations(large_po_path):
    """Load translations from the large .po file into a dictionary."""
    translations = {}
    po = polib.pofile(large_po_path)

    for entry in po:
        if entry.msgid and entry.msgstr:  # Ensure translation exists
            translations[entry.msgid] = entry.msgstr

    return translations


def update_po_file(po_path, translations):
    """Update a given de.po file with matching translations from the large file."""
    po = polib.pofile(po_path)
    updated = False

    for entry in po:
        if entry.msgstr == "Log-Notiz":
            print(po_path)
        if entry.msgid in translations and entry.msgstr != translations[entry.msgid]:
            entry.msgstr = translations[entry.msgid]
            updated = True

    if updated:
        po.save(po_path)  # Save only if changes were made


def find_de_po_files(search_dir):
    """Find all de.po files in subdirectories."""
    de_po_files = []

    for root, _, files in os.walk(search_dir):
        for file in files:
            if file == "de.po":
                de_po_files.append(os.path.join(root, file))

    return de_po_files


def main():
    # Load large.po translations
    translations = load_large_po_translations(LARGE_PO_FILE)

    # Find all de.po files
    po_files = find_de_po_files(SEARCH_DIR)

    if not po_files:
        print("No de.po files found!")
        return

    # Update all de.po files with progress bar
    print(f"Updating {len(po_files)} files...")
    for po_file in tqdm(po_files, desc="Updating de.po files"):
        update_po_file(po_file, translations)

    print("All de.po files updated!")


if __name__ == "__main__":
    main()