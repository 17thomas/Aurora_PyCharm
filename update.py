import requests
import sys

RENDER_URL = "https://aurora-alert-b891.onrender.com"  # change this
LOCAL_DB = "subscribers.db"      # where your real DB lives


def download():
    print("Downloading DB from server...")
    r = requests.get(f"{RENDER_URL}/export_db?token={TOKEN}")
    if r.status_code != 200:
        print("Error:", r.text)
        return
    with open(LOCAL_DB, "wb") as f:
        f.write(r.content)
    print("Saved to", LOCAL_DB)


def upload():
    print("Uploading DB to server...")
    with open(LOCAL_DB, "rb") as f:
        files = {"db": f}
        r = requests.post(f"{RENDER_URL}/import_db?token={TOKEN}", files=files)
    print("Response:", r.text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update.py [download|upload]")
        exit()

    if sys.argv[1] == "download":
        download()
    elif sys.argv[1] == "upload":
        upload()
    else:
        print("Unknown command")
