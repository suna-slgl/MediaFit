import cv2
from flask import Flask, Response
import mediapipe as mp
import math
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def get_reference_from_dataset(csv_path, exercise_label="biceps_curl"):
    df = pd.read_csv(csv_path, comment='#')
    df = df[df['exercise_label'] == exercise_label]
    idx_a, idx_b, idx_c = 11, 13, 15  # Omuz, Dirsek, Bilek
    angles = []
    for _, row in df.iterrows():
        a = [row[f'joint_{idx_a}_x'], row[f'joint_{idx_a}_y']]
        b = [row[f'joint_{idx_b}_x'], row[f'joint_{idx_b}_y']]
        c = [row[f'joint_{idx_c}_x'], row[f'joint_{idx_c}_y']]
        angle = calculate_angle(a, b, c)
        angles.append(angle)
    ref_angle = float(pd.Series(angles).mean())
    tolerance = float(pd.Series(angles).std())
    return ref_angle, tolerance

def gen():
    # csv_path = os.path.join(os.path.dirname(__file__), "../data/raw/sample_keypoints.csv")
    # ref_angle, tolerance = get_reference_from_dataset(csv_path)
    ref_angle = 90  # elle girilen referans açı
    tolerance = 40  # elle girilen tolerans
    ref_angle_high = ref_angle + tolerance
    ref_angle_low = ref_angle - tolerance
    cap = cv2.VideoCapture(0)
    rep_count = 0
    awaiting_down = True
    all_correct = True
    with mp_pose.Pose(static_image_mode=False) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                lm = results.pose_landmarks.landmark
                h, w, _ = frame.shape
                # Sağ kol noktaları
                shoulder = np.array([lm[12].x * w, lm[12].y * h])
                elbow = np.array([lm[14].x * w, lm[14].y * h])
                wrist = np.array([lm[16].x * w, lm[16].y * h])
                # Açı
                angle = calculate_angle(shoulder, elbow, wrist)
                # Doğru aralığı
                correct = ref_angle_low <= angle <= ref_angle_high
                print(f"Canlı açı: {angle:.2f}, Doğru mu: {correct}, Ref: {ref_angle:.2f}, Tol: {tolerance:.2f}")
                # Tekrar sayımı mantığı
                if angle > ref_angle_high:
                    awaiting_down = True
                    all_correct = True
                elif ref_angle_low <= angle <= ref_angle_high:
                    if not correct:
                        all_correct = False
                elif angle < ref_angle_low and awaiting_down:
                    if all_correct:
                        rep_count += 1
                    awaiting_down = False
                # Yazılar
                cv2.putText(frame, f"Açı: {int(angle)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.putText(frame, f"Doğru mu?: {'Evet' if correct else 'Hayır'}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) if correct else (0,0,255), 2)
                cv2.putText(frame, f"Tekrar: {rep_count}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 