from flask import Flask, request, send_file
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Example: Simple background removal using thresholding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)  # Adjust threshold as needed
    result = cv2.bitwise_and(image, image, mask=mask)

    # Save the result to a BytesIO object
    _, buffer = cv2.imencode('.png', result)
    output = BytesIO(buffer)

    return send_file(output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
