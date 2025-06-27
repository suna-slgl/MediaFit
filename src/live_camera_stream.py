import cv2
from flask import Flask, Response, jsonify, request
import mediapipe as mp
import math
import numpy as np
import pandas as pd
import os
import time

app = Flask(__name__)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Kayıt için global değişkenler
recording = False
kayitli_acilar = []  # (timestamp, angle)

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
    print("CSV PATH:", csv_path)
    print("LOOKING FOR EXERCISE:", exercise_label)
    
    try:
        # CSV'yi doğru şekilde oku - engine='python' kullan
        df = pd.read_csv(csv_path, engine='python')
        print("CSV HEAD:")
        print(df.head())
        print("CSV SHAPE:", df.shape)
        print("CSV COLUMNS:", list(df.columns))
        
        # exercise_label sütununun var olup olmadığını kontrol et
        if 'exercise_label' not in df.columns:
            print("HATA: exercise_label sütunu bulunamadı!")
            print("Mevcut sütunlar:", list(df.columns))
            return 170, 15
            
        print("EXERCISE LABEL COLUMN TYPE:", type(df['exercise_label'].iloc[0]))
        print("EXERCISE LABEL COLUMN VALUES:", df['exercise_label'].values)
        print("EXERCISE LABEL UNIQUE:", df['exercise_label'].unique())
        
        # Debug: Her satırın exercise_label değerini kontrol et
        for i, row in df.iterrows():
            print(f"Row {i}: exercise_label = '{row['exercise_label']}' (type: {type(row['exercise_label'])})")
        
        # NaN değerleri temizle
        df = df.dropna(subset=['exercise_label'])
        print("NaN değerler temizlendikten sonra shape:", df.shape)
        
        # String'e çevir ve normalize et
        df['exercise_label'] = df['exercise_label'].astype(str).str.strip().str.lower()
        exercise_label = exercise_label.strip().lower()
        print("NORMALIZED EXERCISE LABEL:", exercise_label)
        print("NORMALIZED CSV LABELS:", df['exercise_label'].values)
        
        # Filtrele
        df = df[df['exercise_label'] == exercise_label]
        print("FILTERED DF SHAPE:", df.shape)
        
        if df.empty:
            print(f"UYARI: CSV'de {exercise_label} etiketiyle veri yok! Fallback ref=170 tol=5 kullanılıyor.")
            return 170, 5  # Biceps curl için sabit tolerans
            
        # Veri setindeki joint indekslerini kullan: 0-32 arası
        # Biceps curl için: Sağ omuz (12), Sağ dirsek (14), Sağ bilek (16)
        idx_a, idx_b, idx_c = 12, 14, 16  # Sağ omuz, Sağ dirsek, Sağ bilek
        
        # Landmark sütunlarının var olup olmadığını kontrol et
        required_columns = [f'joint_{idx_a}_x', f'joint_{idx_a}_y', f'joint_{idx_b}_x', f'joint_{idx_b}_y', f'joint_{idx_c}_x', f'joint_{idx_c}_y']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"HATA: Eksik sütunlar: {missing_columns}")
            return 170, 15
            
        angles = []
        print(f"Veri setinden açı hesaplanıyor...")
        print(f"Kullanılan landmark'lar: Joint {idx_a} (Omuz), Joint {idx_b} (Dirsek), Joint {idx_c} (Bilek)")
        
        for idx, row in df.iterrows():
            # Veri setindeki koordinatları al
            a = [row[f'joint_{idx_a}_x'], row[f'joint_{idx_a}_y']]  # Omuz
            b = [row[f'joint_{idx_b}_x'], row[f'joint_{idx_b}_y']]  # Dirsek (merkez)
            c = [row[f'joint_{idx_c}_x'], row[f'joint_{idx_c}_y']]  # Bilek
            
            angle = calculate_angle(a, b, c)
            angles.append(angle)
            print(f"Frame {row['frame_id']}: Açı = {angle:.2f}° (Omuz: {a}, Dirsek: {b}, Bilek: {c})")
        
        ref_angle = float(pd.Series(angles).mean())
        tolerance = 5.0  # Sabit ±5 derece tolerans
        
        print(f"BULUNAN REF: {ref_angle:.2f}°, TOL: ±{tolerance:.2f}°")
        print(f"Kabul aralığı: {ref_angle-tolerance:.2f}° - {ref_angle+tolerance:.2f}°")
        return ref_angle, tolerance
        
    except Exception as e:
        print(f"CSV OKUMA HATASI: {e}")
        print(f"UYARI: CSV'de {exercise_label} etiketiyle veri yok! Fallback ref=170 tol=5 kullanılıyor.")
        return 170, 5  # Biceps curl için sabit tolerans

@app.route('/start_record', methods=['POST'])
def start_record():
    print("START_RECORD ENDPOINT ÇAĞRILDI")
    global recording, kayitli_acilar
    recording = True
    kayitli_acilar = []
    print(f"START_RECORD: recording={recording}, kayitli_acilar_sayisi={len(kayitli_acilar)}")
    return jsonify({'success': True, 'message': 'Kayıt başladı'})

@app.route('/stop_record', methods=['POST'])
def stop_record():
    try:
        print("STOP_RECORD ENDPOINT ÇAĞRILDI")
        global recording, kayitli_acilar
        recording = False
        print(f"STOP_RECORD: recording={recording}, kayitli_acilar_sayisi={len(kayitli_acilar)}")
        print("Kayıtlı açı sayısı:", len(kayitli_acilar))
        # Referans ve tolerans sample_keypoints.csv'den alınacak
        csv_path = os.path.join(os.path.dirname(__file__), "../data/raw/sample_keypoints.csv")
        ref_angle, tolerance = get_reference_from_dataset(csv_path, exercise_label="biceps_curl")
        ref_angle_high = ref_angle + tolerance
        ref_angle_low = ref_angle - tolerance
        # Doğruluk analizi
        dogru_sayisi = 0
        acilar_json = []
        print(f"DOĞRULUK ANALİZİ:")
        print(f"Referans açı: {ref_angle:.2f}°")
        print(f"Tolerans: ±{tolerance:.2f}°")
        print(f"Kabul aralığı: {ref_angle_low:.2f}° - {ref_angle_high:.2f}°")
        print(f"Kayıtlı açı sayısı: {len(kayitli_acilar)}")
        
        for i, (ts, angle) in enumerate(kayitli_acilar):
            correct = ref_angle_low <= angle <= ref_angle_high
            if correct:
                dogru_sayisi += 1
            print(f"Açı {i+1}: {angle:.2f}° - {'DOĞRU' if correct else 'YANLIŞ'}")
            acilar_json.append({
                'timestamp': ts,
                'angle': angle,
                'correct': bool(correct)
            })
        
        toplam = len(kayitli_acilar)
        dogruluk = (dogru_sayisi / toplam * 100) if toplam > 0 else 0
        print(f"DOĞRU SAYISI: {dogru_sayisi}/{toplam}")
        print(f"DOĞRULUK: {dogruluk:.2f}%")
        # CSV raporu kaydet
        rapor_path = os.path.join(os.path.dirname(__file__), f"../data/raw/egzersiz_raporu_{int(time.time())}.csv")
        with open(rapor_path, 'w') as f:
            f.write('timestamp,angle,correct\n')
            for ts, angle in kayitli_acilar:
                correct = ref_angle_low <= angle <= ref_angle_high
                f.write(f'{ts},{angle:.2f},{int(correct)}\n')
        print("Stop record endpoint JSON dönüyor")
        return jsonify({
            'success': True,
            'dogruluk': dogruluk,
            'kayit_sayisi': toplam,
            'acilar': acilar_json,
            'rapor_path': rapor_path,
            'ref_angle': ref_angle,
            'tolerance': tolerance
        })
    except Exception as e:
        print("Hata:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

def gen():
    print("GEN() FONKSİYONU BAŞLADI")
    csv_path = os.path.join(os.path.dirname(__file__), "../data/raw/sample_keypoints.csv")
    ref_angle, tolerance = get_reference_from_dataset(csv_path, exercise_label="biceps_curl")
    ref_angle_high = ref_angle + tolerance
    ref_angle_low = ref_angle - tolerance
    cap = cv2.VideoCapture(0)
    rep_count = 0
    awaiting_down = True
    all_correct = True
    global recording, kayitli_acilar
    print(f"GEN() BAŞLANGIÇ: recording={recording}, kayitli_acilar_sayisi={len(kayitli_acilar)}")
    with mp_pose.Pose(static_image_mode=False) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("GEN() KAMERA OKUMA HATASI")
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
                # Kayıt modunda açıları kaydet
                if recording:
                    kayitli_acilar.append((time.time(), angle))
                    print(f"GEN() AÇI KAYDEDİLDİ: {angle:.2f}°, Toplam kayıt: {len(kayitli_acilar)}")
                # Doğru aralığı
                correct = ref_angle_low <= angle <= ref_angle_high
                print(f"Canlı açı: {angle:.2f}, Doğru mu: {correct}, Ref: {ref_angle:.2f}, Tol: {tolerance:.2f}, Recording: {recording}")
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