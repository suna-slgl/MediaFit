import pandas as pd
from src.analysis.angle_analysis import calculate_angle, is_movement_correct

# CSV dosyasını oku
df = pd.read_csv("data/raw/sample_keypoints.csv", comment='#')

# Analiz parametreleri
# Biceps curl için: Omuz (11), Dirsek (13), Bilek (15) (MediaPipe indexleri)
shoulder_idx, elbow_idx, wrist_idx = 11, 13, 15
ref_angle = 45  # Örnek referans açı (derece)
tolerance = 15  # Tolerans aralığı

# Sonuçları tutmak için liste
results = []

for idx, row in df.iterrows():
    # Sadece biceps curl frame'leri için örnek
    if row['exercise_label'] != 'biceps_curl':
        continue
    # Eklem noktalarını çek
    a = [row[f'joint_{shoulder_idx}_x'], row[f'joint_{shoulder_idx}_y']]
    b = [row[f'joint_{elbow_idx}_x'], row[f'joint_{elbow_idx}_y']]
    c = [row[f'joint_{wrist_idx}_x'], row[f'joint_{wrist_idx}_y']]
    # Açı hesapla
    angle = calculate_angle(a, b, c)
    # Doğruluk analizi
    correct = is_movement_correct(angle, ref_angle, tolerance)
    results.append({
        "frame_id": row['frame_id'],
        "calculated_angle": angle,
        "is_correct": correct
    })

# Sonuçları DataFrame olarak göster
results_df = pd.DataFrame(results)
print(results_df)
print(f"Doğru yapılan hareket oranı: {results_df['is_correct'].mean()*100:.1f}%")

# Eklem indeksleri MediaPipe standardına göredir (11: omuz, 13: dirsek, 15: bilek).
# Her frame için açı hesaplanır ve referans açı ile karşılaştırılır.
# Sonuçta, her frame’in doğru/tolerans dahilinde olup olmadığı ve genel başarı oranı elde edilir.