import cv2
from flask import Flask, render_template, Response
import sounddevice as sd
import numpy as np
import io
import wave

app = Flask(__name__)

# Capture video from camera
camera = cv2.VideoCapture(0)

# Audio streaming setup
def audio_stream(callback):
    def callback_wrapper(indata, frames, time, status):
        callback(indata.copy())
    with sd.InputStream(callback=callback_wrapper):
        pass  # Continuously streams audio data without the need for an explicit loop

# Generate audio frames
def generate_audio_frames():
    def send_audio(data):
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(data.tobytes())
        yield (b'data:audio/wav;base64,' + buf.getvalue() + b'\n\n')
    audio_stream(callback=send_audio)

# Generate video frames
def generate_video_frames():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Video streaming home page
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Video streaming route
    return Response(generate_video_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio_feed')
def audio_feed():
    # Audio streaming route
    return Response(generate_audio_frames(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
