import time
from detection import detect_from_file
from pathlib import Path
from datetime import datetime
from email_alert import send_email_alert

IMAGE_PATH = Path("images/latest.jpg")

def analyze_image(path: Path):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Analyzing new image")
    detected, green, red = detect_from_file(IMAGE_PATH)
    print(f"Detected: {detected}, Green: {green:.2f}%, Red: {red:.2f}%")

    if detected:
        subject = "Aurora Alert!"
        text = f"Aurora detected!\nGreen: {green:.2f}%\nRed: {red:.2f}%"
        send_email_alert("thomas01.07.2002@gmail.com", subject, text, IMAGE_PATH)


def main():
    last_mtime = None

    while True:
        if IMAGE_PATH.exists():
            mtime = IMAGE_PATH.stat().st_mtime

            # If modified since last check → process it
            if last_mtime is None or mtime > last_mtime:
                last_mtime = mtime
                analyze_image(IMAGE_PATH)

        time.sleep(1)  # check every second

if __name__ == "__main__":
    main()