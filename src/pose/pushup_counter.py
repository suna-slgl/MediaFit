import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

class PushUpCounter:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.counter = 0
        self.stage = None

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def process_frame(self, image, results):
        landmarks = results.pose_landmarks.landmark
        # Sağ kol (örnek)
        shoulder = [landmarks[12].x, landmarks[12].y]
        elbow = [landmarks[14].x, landmarks[14].y]
        wrist = [landmarks[16].x, landmarks[16].y]
        angle = self.calculate_angle(shoulder, elbow, wrist)
        # Tekrar sayımı
        if angle > 160:
            self.stage = "up"
        if angle < 90 and self.stage == "up":
            self.stage = "down"
            self.counter += 1
        return angle

    def reset(self):
        self.counter = 0
        self.stage = None

# Örneğin, 0. eklem noktasının ortalama x ve y'si
df = pd.read_csv("data/raw/sample_keypoints.csv", comment='#')
mean_x = df['joint_0_x'].mean()
mean_y = df['joint_0_y'].mean()
print("Eklem 0 ortalama konumu:", mean_x, mean_y) 