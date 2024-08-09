import os
import json
import pandas as pd


# Function to recursively extract bookmarks from a folder and its subfolders
def extract_bookmarks(bookmarks, extracted_bookmarks=None):
    if extracted_bookmarks is None:
        extracted_bookmarks = []

    for item in bookmarks:
        if item["type"] == "text/x-moz-place":
            link = item.get("uri", "")
            name = item.get("title", "")
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
        elif item["type"] == "text/x-moz-place-container" and "children" in item:
            extract_bookmarks(item["children"], extracted_bookmarks)

    return extracted_bookmarks


# Function to search for a specific folder and extract its bookmarks
def search_folder(bookmarks_data, folder_name):
    def search_folder_recursive(bookmarks, folder_name):
        for item in bookmarks:
            if (
                item["type"] == "text/x-moz-place-container"
                and item["title"] == folder_name
            ):
                return extract_bookmarks(item["children"])
            if "children" in item:
                result = search_folder_recursive(item["children"], folder_name)
                if result:
                    return result
        return None

    folder_bookmarks = search_folder_recursive(bookmarks_data["children"], folder_name)

    if not folder_bookmarks:
        raise ValueError(f"Folder '{folder_name}' not found in bookmarks.")

    return folder_bookmarks


# Function to populate Excel file with bookmarks
def populate_excel(bookmarks, output_file):
    df = pd.DataFrame(
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
        os.remove(output_file)
    else:
        print("Creating new file...")
    df.to_excel(output_file, index=False)
    print(f"Excel file '{output_file}' created successfully.")


# Main function
def main():
    base_path = r"E:\Privat\All Code\Anon\Bookmarks"
    bookmarks_file = os.path.join(base_path, "bookmarks.json")
    output_file = os.path.join(base_path, "bookmarks.xlsx")

    folder_name = "Code"  # Replace with the name of the folder you want to extract

    # Load bookmarks data
    with open(bookmarks_file, "r", encoding="utf-8") as file:
        bookmarks_data = json.load(file)

    # Search for the folder and extract bookmarks
    bookmarks = search_folder(bookmarks_data, folder_name)

    # Populate Excel file
    populate_excel(bookmarks, output_file)


if __name__ == "__main__":
    main()
