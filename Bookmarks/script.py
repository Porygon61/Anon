import os
import json
import pandas as pd
import platform

# Function to recursively extract bookmarks from a folder and its subfolders
def extract_bookmarks(bookmarks, extracted_bookmarks=None):
    if extracted_bookmarks is None:
        extracted_bookmarks = []

    for item in bookmarks:
        if item.get("type") == "url":
            link = item.get("url", "")
            name = item.get("name", "")
            website = link.split("/")[2] if "://" in link else link.split("/")[0]
            extracted_bookmarks.append(
                {
                    "link": link,
                    "rating": "",
                    "Name": name,
                    "genres": "",
                    "website": website,
                    "type": "",  # User will fill this in
                    "real": "",  # User will fill this in
                    "content type": "",  # User will fill this in
                    "notes": "",  # User will fill this in
                }
            )
        elif "children" in item:
            extract_bookmarks(item["children"], extracted_bookmarks)

    return extracted_bookmarks


# Function to search for a specific folder and extract its bookmarks
def search_folder(bookmarks_data, folder_name):
    def search_folder_recursive(bookmarks, folder_name):
        for item in bookmarks:
            if item.get("type") == "folder" and item.get("name") == folder_name:
                return extract_bookmarks(item["children"])
            if "children" in item:
                result = search_folder_recursive(item["children"], folder_name)
                if result:
                    return result
        return None

    folder_bookmarks = search_folder_recursive(bookmarks_data, folder_name)

    if not folder_bookmarks:
        raise ValueError(f"Folder '{folder_name}' not found in bookmarks.")

    return folder_bookmarks


# Function to merge new bookmarks with existing user-inputted data
def merge_with_existing_data(new_data, existing_data):
    # Convert existing data to a dictionary keyed by the 'link'
    existing_dict = {row['link']: row for _, row in existing_data.iterrows()}
    
    # Iterate over the new data and update with existing data where applicable
    for idx, new_row in new_data.iterrows():
        if new_row['link'] in existing_dict:
            # Retain user input fields from existing data
            existing_row = existing_dict[new_row['link']]
            for field in ['rating', 'type', 'real', 'content type', 'notes']:
                new_data.at[idx, field] = existing_row.get(field, "")
    
    return new_data


# Function to populate Excel file with bookmarks
def populate_excel(bookmarks, output_file):
    new_data = pd.DataFrame(
        bookmarks,
        columns=[
            "link",
            "rating",
            "Name",
            "genres",
            "website",
            "type",
            "real",
            "content type",
            "notes",
        ],
    )

    if os.path.exists(output_file):
        # Load existing data
        existing_data = pd.read_excel(output_file)
        # Merge new bookmarks with existing user inputted data
        new_data = merge_with_existing_data(new_data, existing_data)
    
    # Save the updated data to the Excel file
    new_data.to_excel(output_file, index=False)
    print(f"Excel file '{output_file}' updated successfully.")


# Function to find the default path of the Opera or Opera GX bookmarks file
def find_opera_bookmarks_path():
    system = platform.system()
    
    if system == "Windows":
        opera_paths = [
            os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable"),  # Regular Opera
            os.path.expandvars(r"%APPDATA%\Opera Software\Opera GX Stable")  # Opera GX
        ]
    elif system == "Darwin":  # macOS
        opera_paths = [
            os.path.expanduser("~/Library/Application Support/com.operasoftware.Opera"),  # Regular Opera
            os.path.expanduser("~/Library/Application Support/com.operasoftware.OperaGX")  # Opera GX
        ]
    elif system == "Linux":
        opera_paths = [
            os.path.expanduser("~/.config/opera"),  # Regular Opera
            os.path.expanduser("~/.config/opera-gx")  # Opera GX (custom path example, adjust if necessary)
        ]
    else:
        raise Exception("Unsupported OS")

    for path in opera_paths:
        print(f"Checking for Opera bookmarks file at: {path}")
        bookmarks_file = os.path.join(path, "Bookmarks")
        if os.path.exists(bookmarks_file):
            print(f"Bookmarks file found: {bookmarks_file}")
            return bookmarks_file

    raise FileNotFoundError("Opera or Opera GX bookmarks file not found.")


def main():
    output_file = r"E:\Privat\All Code\Anon\Bookmarks\bookmarks.xlsx"  # Update as needed

    folder_name = "Code"  # Replace with the name of the folder you want to extract

    # Find the Opera or Opera GX bookmarks file
    bookmarks_file = find_opera_bookmarks_path()

    # Load bookmarks data
    with open(bookmarks_file, "r", encoding="utf-8") as file:
        bookmarks_data = json.load(file)
    
    # Start searching from the 'bookmark_bar' section or modify as needed
    if 'roots' in bookmarks_data and 'bookmark_bar' in bookmarks_data['roots']:
        start_point = bookmarks_data['roots']['bookmark_bar']['children']
    else:
        raise ValueError("The expected structure in the bookmarks file was not found.")
    
    # Search for the folder and extract bookmarks
    bookmarks = search_folder(start_point, folder_name)

    # Populate Excel file with the extracted bookmarks and retain user inputs
    populate_excel(bookmarks, output_file)


if __name__ == "__main__":
    main()
