from flask import Flask, render_template, request, jsonify
from sr import recog
import socket
#http://127.0.0.1:5000

app = Flask(__name__)

def send_to_pi(data):
    host = 'raspberrypi_ip'  # Replace with your Raspberry Pi's IP address
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runscript', methods=['POST'])
def run_script():
    text_received = recog()
    if text_received:  # Check if any text was received
        response = send_command(text_received)
        return jsonify({"message": text_received, "pi_response": response}), 200
    return jsonify({"error": "No text recognized"}), 400

if __name__ == "__main__":
    app.run(debug=True)
