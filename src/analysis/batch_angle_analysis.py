import pandas as pd
from src.analysis.angle_analysis import calculate_angle, is_movement_correct

# Egzersizlere göre eklem indeksleri ve referans açıları
EXERCISE_CONFIG = {
    'biceps_curl': {
        'indices': (11, 13, 15),  # Omuz, Dirsek, Bilek
        'ref_angle': 45,
        'tolerance': 15
    },
    'pushup': {
        'indices': (12, 14, 16),  # Sağ Omuz, Sağ Dirsek, Sağ Bilek
        'ref_angle': 90,
        'tolerance': 20
    }
}

def analyze_exercise(csv_path, exercise_label):
    df = pd.read_csv(csv_path, comment='#')
    if exercise_label not in EXERCISE_CONFIG:
        raise ValueError(f"Egzersiz yapılandırması bulunamadı: {exercise_label}")
    config = EXERCISE_CONFIG[exercise_label]
    idx_a, idx_b, idx_c = config['indices']
    ref_angle = config['ref_angle']
    tolerance = config['tolerance']
    results = []
    for _, row in df.iterrows():
        if row['exercise_label'] != exercise_label:
            continue
        a = [row[f'joint_{idx_a}_x'], row[f'joint_{idx_a}_y']]
        b = [row[f'joint_{idx_b}_x'], row[f'joint_{idx_b}_y']]
        c = [row[f'joint_{idx_c}_x'], row[f'joint_{idx_c}_y']]
        angle = calculate_angle(a, b, c)
        correct = is_movement_correct(angle, ref_angle, tolerance)
        results.append({
            "frame_id": row['frame_id'],
            "calculated_angle": angle,
            "is_correct": correct
        })
    results_df = pd.DataFrame(results)
    return results_df

if __name__ == "__main__":
    csv_path = "data/raw/sample_keypoints.csv"
    for exercise in EXERCISE_CONFIG.keys():
        print(f"\nEgzersiz: {exercise}")
        results_df = analyze_exercise(csv_path, exercise)
        print(results_df)
        if not results_df.empty:
            print(f"Doğru yapılan hareket oranı: {results_df['is_correct'].mean()*100:.1f}%")
        else:
            print("Veri bulunamadı.") 