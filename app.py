from flask import Flask, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
from image_processing import remove_background, detect_objects
from pdf_generation import generate_pdf_report
import base64
from io import BytesIO
from PIL import Image
import uuid
import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/process-image', methods=['POST'])
def upload_file():
    if 'file' not in request.files and 'file' not in request.form:
        return jsonify({'error': 'No file part'}), 400

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
    else:
        data_url = request.form['file']
        image_data = base64.b64decode(data_url.split(',')[1])
        image = Image.open(BytesIO(image_data))
        filename = 'captured_image.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

    # Generate a unique PDF file name
    unique_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_pdf_filename = f'report_{timestamp}_{unique_id}.pdf'
    output_pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], output_pdf_filename)
    height, width = process_image_and_generate_pdf(filepath, output_pdf_path)
    
    return jsonify({
        'download_url': url_for('download_file', filename=output_pdf_filename),
        'height': float(height),
        'width': float(width)
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

def process_image_and_generate_pdf(image_path, output_pdf_path):
    # Step 1: Remove background and preprocess the image
    processed_image = remove_background(image_path)
    
    # Step 2: Detect objects (feet and coin)
    detection_results = detect_objects(processed_image)
    
    # Step 3: Generate PDF report and get height and width
    height, width = generate_pdf_report(detection_results, output_pdf_path, image_path)
    
    return height, width

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

