from flask import Flask, request, render_template, Response
import cv2
import numpy as np
import os
import random
import base64

app = Flask(__name__)

latest_image = None


@app.route("/")
def index():
    return render_template("stream.html")


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
