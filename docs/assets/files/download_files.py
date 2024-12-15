import os
import re
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

def download_file(url, folder, downloaded_files):
    """Download a file from a URL and save it to the specified folder."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        filename = os.path.basename(url)
        file_path = os.path.join(folder, filename)

        # Check if the file has already been downloaded
        if filename in downloaded_files:
            print(f"Skipped (already downloaded): {file_path}")
            return

        with open(file_path, 'wb') as f:
            f.write(response.content)
        downloaded_files.add(filename)
        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def extract_urls(file_path):
    """Extract URLs from the given text file."""
    urls = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # Find URLs that start with 'https://github.com/user-attachments'
            found_urls = re.findall(r'https://github\.com/user-attachments[^\s()]*', line) # Notepad++ replace link: https://github\.com/user-attachments/[^/]+/[^/]+/
            urls.extend(found_urls)
    return urls

def main():
    if len(sys.argv) != 2:
        print("Usage: Drag and drop a text file onto this script.")
        return

    text_file_path = sys.argv[1]

    if not os.path.isfile(text_file_path):
        print("The specified path is not a valid file.")
        return

    # Create a folder based on the document name
    folder_name = os.path.splitext(os.path.basename(text_file_path))[0]
    folder_path = os.path.join(os.path.dirname(text_file_path), folder_name)

    os.makedirs(folder_path, exist_ok=True)

    urls = extract_urls(text_file_path)

    if not urls:
        print("No valid URLs found.")
        return

    downloaded_files = set()  # Set to track downloaded file names

    # Use ThreadPoolExecutor for concurrent downloading
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_file, url, folder_path, downloaded_files) for url in urls]
        
        # Wait for all futures to complete
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()

# "%programfiles%/git/git-cmd"
# git pull
# git status
# git add .
# git commit -m "New Commit"
# git push origin main
