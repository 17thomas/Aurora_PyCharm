import requests

RENDER_URL = "https://aurora-alert-b891.onrender.com/upload"

def upload_latest(image_path, status="OK"):
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {"status": status}
        r = requests.post(RENDER_URL, files=files, data=data)
        print("Upload response:", r.text)