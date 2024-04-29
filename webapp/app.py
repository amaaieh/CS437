import socket
from flask import Flask, render_template, request, jsonify
from sr import recog
import numpy as np
import cv2
import base64

# http://127.0.0.1:5000

app = Flask(__name__)

latest_image = None


def send_to_pi(data):
    host = "10.0.0.220"  # Replace with your Raspberry Pi's IP address
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data.encode())
        response = s.recv(1024)
        return response.decode()


def send_command(data):
    if data:
        response = send_to_pi(data)
        return response
    return "No command provided"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sr", methods=["POST"])
def sr():
    text_received = recog()
    if text_received:  # Check if any text was received
        print(text_received)
        if (
            ("lock" not in text_received)
            and ("unlock" not in text_received)
            and ("record" not in text_received)
        ):
            return jsonify({"error": "No text recognized"}), 400
        if "unlock" in text_received:
            response = send_command("unlock")
            return jsonify({"message": text_received, "pi_response": response}), 200
        elif "lock" in text_received:
            response = send_command("lock")
            return jsonify({"message": text_received, "pi_response": response}), 200
        elif "record" in text_received:
            response = send_command("record")
            return jsonify({"message": text_received, "pi_response": response}), 200
    return jsonify({"error": "No text recognized"}), 400


@app.route("/talk", methods=["POST"])
def talk():
    #START AUDIO SCRIPT ON THE PI
    response = send_command("start_audio")
    
    #START AUDIO SCRIPT ON THE APP
    return jsonify({"message": "Audio Start", "pi_response": response}), 200
    
@app.route("/toggle_video", methods=["POST"])
def start_video():
    #START UP VIDEO ON PI
    response = send_command("toggle_video")
    return jsonify({"message": "Toggle Video", "pi_response": response}), 200

@app.route("/receive_image", methods=["POST"])
def receive_image():
    global latest_image

    image = request.files["image"].read()
    nparr = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # SAVE FILE as image in a data folder
    # random_num = random.randint(1, 1000)
    # filename = os.path.join("data/", f"captured_image_{random_num}.jpg")
    # cv2.imwrite(filename, img)

    # DISPLAY IMG on flask application
    retval, buffer = cv2.imencode(".jpg", img)
    encoded_image = base64.b64encode(buffer).decode("utf-8")

    # Update the latest image
    latest_image = encoded_image

    return "Image received successfully!"


@app.route("/get_latest_image")
def get_latest_image():
    global latest_image

    # Serve the latest image
    if latest_image == None:
        return "-1"
    else:
        return latest_image


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
