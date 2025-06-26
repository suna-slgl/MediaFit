import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from angle_analysis import calculate_angle, is_movement_correct
import cv2
import mediapipe as mp
import numpy as np


# Egzersiz ayarları (örnek: biceps curl)
EXERCISE = "biceps_curl"
JOINTS = (11, 13, 15)  # Omuz, Dirsek, Bilek (MediaPipe)
REF_ANGLE = 45
TOLERANCE = 15

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # BGR'dan RGB'ye çevir
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            a = [landmarks[JOINTS[0]].x * frame.shape[1], landmarks[JOINTS[0]].y * frame.shape[0]]
            b = [landmarks[JOINTS[1]].x * frame.shape[1], landmarks[JOINTS[1]].y * frame.shape[0]]
            c = [landmarks[JOINTS[2]].x * frame.shape[1], landmarks[JOINTS[2]].y * frame.shape[0]]
            angle = calculate_angle(a, b, c)
            correct = is_movement_correct(angle, REF_ANGLE, TOLERANCE)

            # Görüntüye açı ve doğruluk bilgisini yaz
            cv2.putText(image, f"Aci: {int(angle)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.putText(image, f"Dogru mu?: {'Evet' if correct else 'Hayir'}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) if correct else (0,0,255), 2)
        except Exception as e:
            pass

        # Anahtar noktaları çiz
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('MediaFit Canli Aci Analizi', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()