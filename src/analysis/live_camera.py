import sys
import cv2
import mediapipe as mp
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QFont
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from angle_analysis import calculate_angle, is_movement_correct

# Egzersiz ayarları
EXERCISE_CONFIG = {
    'Biceps Curl': {
        'joints': (11, 13, 15),
        'ref_angle': 45,
        'tolerance': 15
    },
    'Pushup': {
        'joints': (12, 14, 16),
        'ref_angle': 90,
        'tolerance': 20
    }
}

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    angle_signal = pyqtSignal(float, bool)

    def __init__(self, exercise_name):
        super().__init__()
        self._run_flag = True
        self.exercise_name = exercise_name

    def run(self):
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(0)
        config = EXERCISE_CONFIG[self.exercise_name]
        joints = config['joints']
        ref_angle = config['ref_angle']
        tolerance = config['tolerance']
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self._run_flag:
                ret, frame = cap.read()
                if not ret:
                    continue
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    a = [landmarks[joints[0]].x * frame.shape[1], landmarks[joints[0]].y * frame.shape[0]]
                    b = [landmarks[joints[1]].x * frame.shape[1], landmarks[joints[1]].y * frame.shape[0]]
                    c = [landmarks[joints[2]].x * frame.shape[1], landmarks[joints[2]].y * frame.shape[0]]
                    angle = calculate_angle(a, b, c)
                    correct = is_movement_correct(angle, ref_angle, tolerance)
                    self.angle_signal.emit(angle, correct)
                except Exception:
                    self.angle_signal.emit(-1, False)
                # Anahtar noktaları çiz
                if results.pose_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                # Görüntüyü PyQt formatına çevir
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.change_pixmap_signal.emit(qt_image)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MediaFit")
        self.setGeometry(200, 200, 900, 700)
        label_font = QFont()
        label_font.setPointSize(12) 
        self.exercise_combo = QComboBox()
        self.exercise_combo.addItems(list(EXERCISE_CONFIG.keys()))
        self.camera_label = QLabel("LIVE")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: #ddd; min-height: 400px;")
        self.angle_label = QLabel("Açı: -")
        self.angle_label.setFont(label_font)
        self.start_button = QPushButton("Başlat")
        self.stop_button = QPushButton("Durdur")
        self.stop_button.setEnabled(False)
        layout = QVBoxLayout()
        layout.addWidget(self.exercise_combo)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.angle_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.thread = None
        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)
    def start_camera(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        exercise = self.exercise_combo.currentText()
        self.thread = CameraThread(exercise)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.angle_signal.connect(self.update_angle)
        self.thread.start()
    def stop_camera(self):
        if self.thread:
            self.thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    def update_image(self, qt_image):
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.camera_label.width(), self.camera_label.height(), Qt.KeepAspectRatio))
    def update_angle(self, angle, correct):
        if angle == -1:
            self.angle_label.setText("Açı: -")
        else:
            self.angle_label.setText(f"Açı: {angle:.1f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())