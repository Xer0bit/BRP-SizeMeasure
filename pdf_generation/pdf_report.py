import logging
import cv2
import numpy as np
from fpdf import FPDF
from image_processing.background_removal import remove_background
from image_processing.object_detection import detect_objects

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Feet Measurement Report', 0, 1, 'C')
        self.ln(10)

    def add_image_with_marks(self, image, feet_boxes, coin_box, mm_per_pixel):
        """
        Add an image with marked feet and coin to the PDF.

        Parameters:
        image (numpy.ndarray): The image to be marked and added.
        feet_boxes (list): List of bounding boxes for feet.
        coin_box (list): Bounding box for the coin.
        mm_per_pixel (float): Millimeters per pixel.
        """
        try:
            # Draw green lines and add measurements for feet
            for i, box in enumerate(feet_boxes):
                x1, y1, x2, y2 = map(int, box)
                width_cm = (x2 - x1) * mm_per_pixel / 10
                height_cm = (y2 - y1) * mm_per_pixel / 10
                
                # Draw rectangle around the feet
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Add text for measurements
                text = f'W: {width_cm:.1f} cm, H: {height_cm:.1f} cm'
                cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Add cross mark for the coin if detected
            if coin_box is not None:
                x1, y1, x2, y2 = map(int, coin_box)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.drawMarker(image, (cx, cy), (255, 0, 0), markerType=cv2.MARKER_CROSS, markerSize=50, thickness=6)
            
            # Save the image to a temporary file
            temp_image_path = 'temp_detected_image.jpg'
            cv2.imwrite(temp_image_path, image)

            # Add image to PDF in color
            self.image(temp_image_path, x=50, y=90, w=120)  # Adjust width as needed

        except Exception as e:
            logging.error(f"An error occurred while adding the image with marks: {e}")
            raise

    def add_feet_measurements(self, detection_results, coin_diameter_mm):
        """
        Add feet measurements to the PDF.
        
        Parameters:
        detection_results (dict): The detection results containing feet and coin boxes.
        coin_diameter_mm (float): The diameter of the coin in millimeters.
        """
        try:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Feet Measurements:', 0, 1, 'L')
            self.set_font('Arial', '', 12)
            
            if detection_results['coin_box'] is not None:
                coin_box = detection_results['coin_box']
                coin_diameter_pixels = coin_box[2] - coin_box[0]  # Assuming the coin's width is its diameter
                mm_per_pixel = coin_diameter_mm / coin_diameter_pixels
                
                for i, box in enumerate(detection_results['feet_boxes']):
                    x1, y1, x2, y2 = map(int, box)
                    width_cm = (x2 - x1) * mm_per_pixel / 10
                    height_cm = (y2 - y1) * mm_per_pixel / 10
                    self.cell(0, 10, f'  Foot {i+1}:', 0, 1, 'L')
                    self.cell(0, 10, f'    Width: {width_cm:.2f} cm', 0, 1, 'L')
                    self.cell(0, 10, f'    Height: {height_cm:.2f} cm', 0, 1, 'L')
                    self.ln(5)
            else:
                self.cell(0, 10, 'Coin not detected. Unable to calculate measurements.', 0, 1, 'L')
        except Exception as e:
            logging.error(f"An error occurred while adding feet measurements: {e}")
            raise

def return_height_width(detection_results, coin_diameter_mm):
    try:
        if detection_results['coin_box'] is not None:
            coin_box = detection_results['coin_box']
            coin_diameter_pixels = coin_box[2] - coin_box[0]  # Assuming the coin's width is its diameter
            mm_per_pixel = coin_diameter_mm / coin_diameter_pixels

            for box in detection_results['feet_boxes']:
                x1, y1, x2, y2 = map(int, box)
                width_cm = (x2 - x1) * mm_per_pixel / 10
                height_cm = (y2 - y1) * mm_per_pixel / 10
                return float(height_cm), float(width_cm)
        return 0.0, 0.0
    except Exception as e:
        logging.error(f"An error occurred while calculating height and width: {e}")
        raise

def generate_pdf_report(detection_results, output_pdf_path, original_image_path, coin_diameter_mm=25.75):
    """
    Generate a PDF report with feet measurements and marked images.

    Parameters:
    detection_results (dict): The detection results containing feet and coin boxes.
    output_pdf_path (str): The path to save the generated PDF.
    original_image_path (str): The path to the original image.
    coin_diameter_mm (float): The diameter of the coin in millimeters.
    """
    try:
        pdf = PDFReport()
        pdf.add_page()
        
        # Calculate mm_per_pixel
        if detection_results['coin_box'] is not None:
            coin_box = detection_results['coin_box']
            coin_diameter_pixels = coin_box[2] - coin_box[0]  # Assuming the coin's width is its diameter
            mm_per_pixel = coin_diameter_mm / coin_diameter_pixels
        else:
            mm_per_pixel = 1  # Fallback value if coin is not detected
        
        # Load original image and remove background
        processed_image = remove_background(original_image_path)
        detection_results['image'] = processed_image
        
        # Add image with green lines marking the feet dimensions
        pdf.add_image_with_marks(detection_results['image'], detection_results['feet_boxes'], detection_results['coin_box'], mm_per_pixel)
        
        # Add feet measurements
        pdf.add_feet_measurements(detection_results, coin_diameter_mm)
        height, width = return_height_width(detection_results, coin_diameter_mm)
        
        pdf.output(output_pdf_path)
        logging.info(f"PDF report generated successfully and saved to {output_pdf_path}")
        return height, width
    except Exception as e:
        logging.error(f"An error occurred while generating the PDF report: {e}")
        raise

