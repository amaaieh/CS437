import speech_recognition
import time

def recog():
    recognizer = speech_recognition.Recognizer()

    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                print("Listening...")
                audio = recognizer.listen(mic)

                text = recognizer.recognize_google(audio)
                text = text.lower()

                print(f"Recognized: {text}")
                return text  # Return the recognized text and exit the loop

        except speech_recognition.UnknownValueError:
            print("Could not understand audio")
        except speech_recognition.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

        # Check if 10 seconds have passed since the start of the loop
        # if time.time() - start_time >= 3:
        #     print("Timeout: No speech detected within 10 seconds")
        #     return None  # Return None if no speech is detected within 10 seconds

    return "function heard nothing"


# recog()