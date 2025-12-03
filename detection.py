import cv2
import numpy as np
from pathlib import Path


def detect_aurora(image):
    """
    Detect auroras based on green and red filters using percentage thresholds.

    Args:
        image (numpy.ndarray): BGR image loaded with cv2.imread()

    Returns:
        detected (bool): True if aurora is detected
        green_percentage (float): percentage of green pixels in circular mask
        red_percentage (float): percentage of red pixels in circular mask
    """
    # Convert BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width = image.shape[:2]

    # Define HSV ranges for green
    green_lower = (40, 8, 40)
    green_upper = (80, 255, 255)

    # Define HSV ranges for red (two ranges: low red and high red)
    red_lower1 = (0, 35, 40)
    red_upper1 = (10, 255, 255)
    red_lower2 = (160, 35, 40)
    red_upper2 = (180, 255, 255)

    # Create a circular mask
    center = (width // 2, int((height // 2) * 0.97))
    radius = int(min(width, height) // 2.2)
    circular_mask = np.zeros((height, width), dtype=np.uint8)
    cv2.circle(circular_mask, center, radius, 255, -1)

    # Create masks for green and red
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Apply circular mask
    green_mask_circular = cv2.bitwise_and(green_mask, circular_mask)
    red_mask_circular = cv2.bitwise_and(red_mask, circular_mask)

    # Count non-zero pixels
    green_pixels = cv2.countNonZero(green_mask_circular)
    red_pixels = cv2.countNonZero(red_mask_circular)

    # Percentages using circular area
    circular_area = np.count_nonzero(circular_mask)
    green_percentage = (green_pixels / circular_area) * 100
    red_percentage = (red_pixels / circular_area) * 100

    # Thresholds
    green_threshold = -1
    red_threshold = 100
    detected = green_percentage > green_threshold or red_percentage > red_threshold

    return detected, green_percentage, red_percentage


# Optional: helper to run on a single image file
def detect_from_file(image_path: Path):
    """
    Load image from path and detect aurora.
    """
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Image could not be loaded: {image_path}")
    return detect_aurora(image)
