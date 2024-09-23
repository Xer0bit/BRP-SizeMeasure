import logging
from ultralytics import YOLO
import cv2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_objects(image):
    """
    Detect feet and coin objects in the given image using YOLO models.
    
    Parameters:
    image (numpy.ndarray): The input image in which objects need to be detected.
    
    Returns:
    dict: A dictionary containing the original image, detected feet bounding boxes, and the highest confidence coin bounding box.
    """
    try:
        logging.info("Loading YOLO models for feet and coin detection.")
        feet_model = YOLO('models/best.pt')
        coin_model = YOLO('models/coin.pt')
        
        logging.info("Detecting feet in the image.")
        feet_results = feet_model(image)
        feet_boxes = feet_results[0].boxes.xyxy
        
        logging.info("Detecting coins in the image.")
        coin_results = coin_model(image)
        coin_boxes = coin_results[0].boxes.xyxy
        
        coin_box = None
        if len(coin_boxes) > 0:
            logging.info("Selecting the coin with the highest confidence.")
            coin_box = coin_boxes[0]  # Assuming boxes are sorted by confidence
        
        return {'image': image, 'feet_boxes': feet_boxes, 'coin_box': coin_box}

    except Exception as e:
        logging.error(f"An error occurred during object detection: {e}")
        raise

