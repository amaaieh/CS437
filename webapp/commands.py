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
        if video_process == None:
            # start up detect2.py script
            print("starting video feed")
            script_path = "/home/zach/raspberry_pi/detect2.py"
            video_process = subprocess.Popen(
                ["python3", script_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            # stop video script
            print("stopping video feed")
            video_process.terminate()
            video_process = None

    elif data == "toggle_audio":
        if audio_process == None:
            # start up one_way_voice.py script
            print("starting audio script")
            script_path = "/home/zach/RingDoorbell/one_way_voice.py"
            audio_process = subprocess.Popen(
                ["python3", script_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            # stop audio script
            print("stopping video feed")
            audio_process.terminate()
            audio_process = None

    return None
