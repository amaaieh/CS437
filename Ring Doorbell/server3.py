import cv2
from flask import Flask, render_template, Response

video = cv2.VideoCapture(0)
app = Flask(__name__)


def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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
