import logging
import cv2
import numpy as np
from rembg import remove

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_image(image_path):
    """
    Load an image from the given path and remove its background.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    numpy.ndarray: The processed image with background removed.
    """
    try:
        logging.info(f"Loading image from path: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from path: {image_path}")
        
        logging.info("Removing background from the image.")
        image = remove(image, alpha=1)
        
        logging.info("Converting image from RGBA to RGB.")
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        return image
    except Exception as e:
        logging.error(f"An error occurred while loading the image: {e}")
        raise

def get_rotation_angle(image):
    """
    Detect the rotation angle of the given image using the Hough Line Transform.

    Parameters:
    image (numpy.ndarray): The input image.

    Returns:
    float: The detected rotation angle.
    """
    try:
        logging.info("Converting image to grayscale.")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        logging.info("Detecting edges using Canny edge detector.")
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        logging.info("Detecting lines using Hough Line Transform.")
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        if lines is not None:
            logging.info("Calculating angles of detected lines.")
            angles = [(theta * 180 / np.pi) - 90 for rho, theta in lines[:, 0]]
            median_angle = np.median(angles)
            return median_angle
        else:
            logging.warning("No lines detected, returning angle 0.")
            return 0
    except Exception as e:
        logging.error(f"An error occurred while detecting rotation angle: {e}")
        raise

def auto_rotate_image(image_path):
    """
    Automatically rotate an image to correct its orientation if the angle is within ±10 degrees.

    Parameters:
    image_path (str): The path to the image file.

    Returns:
    tuple: A tuple containing the processed image and the detected rotation angle.
    """
    try:
        image = load_image(image_path)
        
        angle = get_rotation_angle(image)
        logging.info(f"Detected rotation angle: {angle:.2f} degrees")
        
        # Check if rotation is needed based on the detected angle
        if abs(angle) > 10:
            logging.info(f"Angle {angle} is greater than 10 degrees, no rotation will be applied.")
            rotated_image = image  # No rotation applied
        else:
            logging.info(f"Angle {angle} is within ±10 degrees, rotating the image.")
            rotated_image = rotate_image(image, angle)
        
        return rotated_image, angle
    except Exception as e:
        logging.error(f"An error occurred in auto_rotate_image: {e}")
        raise


def rotate_image(image, angle):
    """
    Rotate the given image by the specified angle.

    Parameters:
    image (numpy.ndarray): The input image.
    angle (float): The angle to rotate the image.

    Returns:
    numpy.ndarray: The rotated image.
    """
    try:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        
        logging.info(f"Rotating image by {angle:.2f} degrees.")
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        
        return rotated
    except Exception as e:
        logging.error(f"An error occurred while rotating the image: {e}")
        raise

