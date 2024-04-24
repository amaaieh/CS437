import cv2
from flask import Flask, render_template, Response
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()

app = Flask(__name__)


def video_stream():
    while True:
        image = picam2.capture_array()
        if not image:
            break
        else:
            picam2.capture_file("capture.jpg")
            image_bytes = 1
            with open("capture.jpg", 'rb') as f:
                image_bytes = f.read()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')


@app.route('/')
def index():
    # Render the camera.html template, which contains the video feed
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    # Return the video stream response
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
