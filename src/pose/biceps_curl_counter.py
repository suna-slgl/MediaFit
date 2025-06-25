import cv2
import mediapipe as mp
import numpy as np

class BicepsCurlCounter:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.counter_left = 0
        self.counter_right = 0
        self.stage_left = None
        self.stage_right = None

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
        # Sol kol
        shoulder_left = [landmarks[11].x, landmarks[11].y]
        elbow_left = [landmarks[13].x, landmarks[13].y]
        wrist_left = [landmarks[15].x, landmarks[15].y]
        angle_left = self.calculate_angle(shoulder_left, elbow_left, wrist_left)
        # Sağ kol
        shoulder_right = [landmarks[12].x, landmarks[12].y]
        elbow_right = [landmarks[14].x, landmarks[14].y]
        wrist_right = [landmarks[16].x, landmarks[16].y]
        angle_right = self.calculate_angle(shoulder_right, elbow_right, wrist_right)
        # Sol kol tekrar sayımı
        if angle_left > 160:
            self.stage_left = "down"
        if angle_left < 40 and self.stage_left == "down":
            self.stage_left = "up"
            self.counter_left += 1
        # Sağ kol tekrar sayımı
        if angle_right > 160:
            self.stage_right = "down"
        if angle_right < 40 and self.stage_right == "down":
            self.stage_right = "up"
            self.counter_right += 1
        return angle_left, angle_right

    def reset(self):
        self.counter_left = 0
        self.counter_right = 0
        self.stage_left = None
        self.stage_right = None 