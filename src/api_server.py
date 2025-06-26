from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import mediapipe as mp
import numpy as np
import math

app = Flask(__name__)

def calculate_angle(a, b, c):
    # a, b, c: (x, y) tuple
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if 'image' not in data:
        return jsonify({'success': False, 'message': 'Resim verisi yok'}), 400
    try:
        # Base64'ten resmi çöz
        image_data = base64.b64decode(data['image'])
        # YUV420 formatı için sadece ilk plane kullanıldı, gerçek uygulamada JPEG beklenmeli
        # Burada örnek olarak PNG/JPEG bekleniyor
        image = Image.open(BytesIO(image_data)).convert('RGB')
        np_image = np.array(image)
        mp_pose = mp.solutions.pose
        with mp_pose.Pose(static_image_mode=True) as pose:
            results = pose.process(np_image)
            if results.pose_landmarks:
                # Örnek: Sağ dirsek açısı (shoulder, elbow, wrist)
                lm = results.pose_landmarks.landmark
                right_shoulder = (lm[12].x, lm[12].y)
                right_elbow = (lm[14].x, lm[14].y)
                right_wrist = (lm[16].x, lm[16].y)
                angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                # Basit doğruluk: açı 160-180 arası ise doğru kabul
                correct = bool(160 <= angle <= 180)
                return jsonify({
                    'success': True,
                    'message': 'Analiz tamamlandı',
                    'right_elbow_angle': angle,
                    'is_correct': correct,
                    'landmarks': [
                        {'x': lmk.x, 'y': lmk.y, 'z': lmk.z, 'visibility': lmk.visibility}
                        for lmk in results.pose_landmarks.landmark
                    ]
                })
            else:
                return jsonify({'success': False, 'message': 'İnsan bulunamadı'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 