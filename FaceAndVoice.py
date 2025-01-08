import cv2
import sqlite3
import numpy as np
import pyttsx3
import speech_recognition as sr
import time
import mysql.connector
from PIL import Image

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Database Connection
DB_HOST = "localhost"      
DB_USER = "root"   
DB_PASSWORD = "Shreya@14"  
DB_NAME = "mydata"          
TABLE_NAME = "register"     

def fetch_registered_faces():
    """Fetch registered faces from the database."""
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="Shreya@14", database="mydata")
        cursor = conn.cursor()
        cursor.execute(f"SELECT image, fname, lname FROM {TABLE_NAME}")
        faces = cursor.fetchall()
        conn.close()

        images = []
        labels = []
        names = {}
        
        for index, (image_data, fname, lname) in enumerate(faces):
            if image_data:
                img_array = np.frombuffer(image_data, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)  # Decode as grayscale
                if img is not None:
                    images.append(img)
                    labels.append(index)  # Use index as label
                    names[index] = f"{fname} {lname}"  # Store name by index

        return images, labels, names
    except Exception as e:
        print(f"Database error: {e}")
        return [], [], {}

# Voice Recognition Function
def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.energy_threshold = 300  # Adjust as needed
        recognizer.dynamic_energy_threshold = True

        speak("Please say your passphrase.")
        print("Listening for passphrase...")
        try:
            audio = recognizer.listen(source, timeout=5)  # 5 seconds to speak
            passphrase = recognizer.recognize_google(audio).strip().lower()
            print(f"Recognized passphrase: {passphrase}")
            return passphrase
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            print("Speech not understood.")
            return None
        except sr.RequestError:
            speak("Voice recognition service is unavailable.")
            print("Voice recognition service unavailable.")
            return None

# Authentication Configuration
AUTHORIZED_PASSPHRASE = "shreya jha"
AUTHORIZED_FACE_AREA_THRESHOLD = 5000  # Minimum bounding box area for valid face detection

# Load Registered Faces
images, labels, names = fetch_registered_faces()

# Initialize LBPH Face Recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, np.array(labels))

# Set up the video capture
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not open camera.")
    exit()

# Track success status
access_granted = False

# Main Loop
time.sleep(2)
while not access_granted:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame from camera. Exiting...")
        break

    # Convert frame to grayscale for face detection and recognition
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load OpenCV's pre-trained face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    face_detected = False

    for (x, y, w, h) in faces:
        face_detected = True
        roi_gray = gray_frame[y:y+h, x:x+w]

        # Recognize face using LBPH
        label, confidence = recognizer.predict(roi_gray)

        if confidence < 100:  # Confidence threshold for a match
            name = names[label]
            speak(f"Face recognized as {name}. Please confirm your identity with your voice.")
            time.sleep(0.5)

            # Perform Voice Recognition
            passphrase = recognize_voice()
            if passphrase == AUTHORIZED_PASSPHRASE:
                speak("Access granted. Door unlocked.")
                print("Access granted. Door unlocked.")
                access_granted = True
                break
            else:
                speak("Voice not recognized. Access denied.")
                print("Voice not recognized. Access denied.")
        else:
            speak("Face not recognized. Access denied.")
            print("Face not recognized. Access denied.")

    if not face_detected:
        print("No face detected.")

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Handle keypresses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Exiting...")
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
