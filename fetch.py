import requests
from pathlib import Path
from datetime import datetime
import time

IMAGE_URL = "https://kho.unis.no/Quicklooks/kho_sony.jpg"
SAVE_DIR = Path("images")
SAVE_DIR.mkdir(exist_ok=True)
SAVE_DIR2 = Path("web/static")
SAVE_DIR2.mkdir(exist_ok=True)

def download_image():
    try:
        response = requests.get(IMAGE_URL, timeout=10)
        response.raise_for_status()

        # latest image
        latest_path = SAVE_DIR / "latest.jpg"
        latest_path.write_bytes(response.content)

        latest_path = SAVE_DIR2 / "latest.jpg"
        latest_path.write_bytes(response.content)

        # archive image
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        archive_path = SAVE_DIR / f"{timestamp}_KHO_Image.jpg"
        archive_path.write_bytes(response.content)

        print(f"Saved latest.jpg and archive {archive_path.name}")
    except Exception as e:
        print("Error downloading image:", e)

def main():
    while True:
        download_image()
        time.sleep(60)

if __name__ == "__main__":
    main()
