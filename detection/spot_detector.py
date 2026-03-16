import cv2

def is_occupied(spot_img, threshold=100):
    """
    Determine if a parking spot is occupied based on mean grayscale intensity.

    Args:
        spot_img: Cropped image of the parking spot (numpy array).
        threshold: Intensity threshold below which the spot is considered occupied.

    Returns:
        bool: True if occupied, False if free.
    """
    if spot_img.size == 0:
        return False  # Assume free if invalid crop

    # Convert to grayscale and check mean intensity
    gray = cv2.cvtColor(spot_img, cv2.COLOR_BGR2GRAY)
    mean_val = cv2.mean(gray)[0]

    # Threshold: if mean intensity < threshold, consider occupied (darker = vehicle)
    return mean_val < threshold