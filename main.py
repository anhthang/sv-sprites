import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# The URL of the page to scrape
URL = "https://projectpokemon.org/home/docs/spriteindex_148/switch-sv-style-sprites-for-home-r153/"
# Folder to save the sprites
SAVE_FOLDER = "sprites"


def download_sprites():
    # Create the directory if it doesn't exist
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"Created folder: {SAVE_FOLDER}")

    # Set a User-Agent to avoid being blocked by the server
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    print("Fetching page content...")
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all images. Project Pokemon (Invision Community) often uses 'data-src' for lazy loading.
    images = soup.find_all("img")

    downloaded_count = 0

    print("Starting download...")
    for img in images:
        # Check 'data-src' first (for lazy loading), then 'src'
        img_url = img.get("data-src") or img.get("src")

        if not img_url:
            continue

        # Filter for sprites: they are usually PNGs and follow a numeric naming convention (e.g., 0001.png)
        # We also want to exclude small icons like avatars or UI elements
        filename = img_url.split("/")[-1]

        # Condition: Ends with .png and the filename contains numeric patterns seen on the page
        # (The script looks for filenames like '0001.png' or '0001_01.png')
        if filename.endswith(".png") and any(char.isdigit() for char in filename):
            # Resolve relative URLs to absolute
            full_url = urljoin(URL, img_url)

            try:
                img_data = requests.get(full_url, headers=headers).content
                with open(os.path.join(SAVE_FOLDER, filename), "wb") as handler:
                    handler.write(img_data)
                downloaded_count += 1
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Failed to download {filename}: {e}")

    print(f"\nFinished! Total sprites downloaded: {downloaded_count}")


if __name__ == "__main__":
    download_sprites()
