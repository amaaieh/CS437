import picar_4wd as fc
import sys
import tty
import termios
import asyncio
import time
import subprocess

power_val = 50
video_process = None
audio_process = None


def command_response(data):
    global video_process
    global audio_process

    if data == "lock":
        fc.forward(power_val)
        time.sleep(0.5)
        fc.stop()
    elif data == "unlock":
        fc.backward(power_val)
        time.sleep(0.5)
        fc.stop()
    elif data == "toggle_video":
        # start up detect2.py script
        if video_process == None:
            print("starting video feed")
            script_path = "/home/zach/raspberry_pi/detect2.py"
            video_process = subprocess.Popen(
                ["python3", script_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            print("stopping video feed")
            video_process.terminate()
            video_process = None
    elif data == "start_audio":
        print("starting audio")
        pass
    return None
