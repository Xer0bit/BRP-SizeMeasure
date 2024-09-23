# Feet Measurement Report Generator

This project calculates foot sizes using a reference coin and generates a PDF report with measurements of detected feet from an image. The report includes marked images and calculated dimensions, providing a detailed analysis of the detected objects.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Example Images](#example-images)
- [File Structure](#file-structure)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Features

- **Background Removal**: Removes the background from the input image.
- **Object Detection**: Detects feet and coins using YOLO models.
- **Feet Measurements**: Calculates the width and height of the detected feet in centimeters.
- **PDF Report Generation**: Creates a PDF report with marked images and measurements.

## Requirements

- Python 3.7+
- OpenCV
- NumPy
- fpdf
- matplotlib
- ultralytics
- flask
- rembg

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/xer0bit/feet-measurement-report-generator.git
    cd feet-measurement-report-generator
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare your YOLO models**:
    Ensure you have the YOLO models for detecting feet and coins in the `models/` directory:
    - `models/feet.pt`
    - `models/coin.pt`

2. **Run the script**:
    ```python
    from image_processing import remove_background, detect_objects
    from pdf_report import generate_pdf_report

    # Example usage
    original_image_path = 'path/to/original/image.jpg'
    detection_results = detect_objects(remove_background(original_image_path))
    output_pdf_path = 'path/to/output/report.pdf'
    generate_pdf_report(detection_results, output_pdf_path, original_image_path)
    ```

3. **View the generated PDF**:
    The PDF report will be saved to the path specified in `output_pdf_path`.

## Example Images

### Input Image
![Input Image](https://github.com/Xer0bit/BRP-SizeMeasure/blob/main/temp/aed3f5b6-66be-49cb-85b7-8d26701dc2a5/input.png)

### Output PDF Report (Final Result)
![Output PDF Report](https://github.com/Xer0bit/BRP-SizeMeasure/blob/main/temp/aed3f5b6-66be-49cb-85b7-8d26701dc2a5/output.png)

## File Structure

- **`models/`**: Directory containing the YOLO model files.
- **`image_processing.py`**: Script for image loading, background removal, and object detection.
- **`pdf_report.py`**: Script for generating the PDF report.
- **`requirements.txt`**: List of required Python packages.
- **`README.md`**: Project documentation.
- **`example_usage.py`**: Example script demonstrating how to use the project.

## Acknowledgments

- [YOLO](https://github.com/ultralytics/yolov5) for the object detection models.
- [OpenCV](https://opencv.org/) and [NumPy](https://numpy.org/) for image processing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
