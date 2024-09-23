import logging
import cv2
import numpy as np
from rembg import remove
from .utils import auto_rotate_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_background(image_path):
    """
    Remove the background from an image and apply some post-processing steps.
    
    Parameters:
    image_path (str): The file path to the image.
    
    Returns:
    numpy.ndarray: The processed image.
    """
    try:
        logging.info(f"Reading the image from path: {image_path}")
        image, detected_angle = auto_rotate_image(image_path)
        
        # Determine if rotation is needed based on the detected angle
        if abs(detected_angle) > 10:
            logging.info(f"Angle {detected_angle} is greater than 10 degrees, not rotating the image.")
            angle = 0
        else:
            logging.info(f"Angle {detected_angle} is between -10 and 10 degrees, rotating the image.")
            angle = detected_angle
            image = rotate_image(image, angle)
        
        logging.info("Removing the background from the image.")
        result = remove(image, alpha=1)

        logging.info("Ensuring the image is in RGB format.")
        if result.shape[2] == 4:  # Check if the image has an alpha channel
            image_rgb = cv2.cvtColor(result, cv2.COLOR_RGBA2RGB)
        else:
            image_rgb = result  # Already in RGB

        logging.info("Applying sharpness enhancement to the image.")
        image_sharp = cv2.convertScaleAbs(image_rgb, alpha=1.5, beta=4)
        
        return image_sharp

    except Exception as e:
        logging.error(f"An error occurred while processing the image: {e}")
        raise

def rotate_image(image, angle):
    """
    Rotate the image to the specified angle.
    
    Parameters:
    image (numpy.ndarray): The image to rotate.
    angle (float): The angle to rotate the image.
    
    Returns:
    numpy.ndarray: The rotated image.
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

