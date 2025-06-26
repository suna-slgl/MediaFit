import numpy as np

def calculate_angle(a, b, c):
    """
    Üç eklem noktası (a, b, c) ile b açısını derece cinsinden hesaplar.
    a, b, c: [x, y] şeklinde numpy array veya liste
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

def is_movement_correct(angle, ref_angle, tolerance=15):
    """
    Hesaplanan açı ile referans açı arasındaki fark tolerans dahilindeyse True döner.
    """
    return abs(angle - ref_angle) <= tolerance

# Örnek kullanım:
if __name__ == "__main__":
    # Örnek eklem noktaları (x, y)
    a = [0.5, 0.2]  # Omuz
    b = [0.55, 0.25]  # Dirsek
    c = [0.6, 0.3]  # Bilek
    angle = calculate_angle(a, b, c)
    print(f"Hesaplanan açı: {angle:.2f} derece")
    # Referans açı örneği (ör: 45 derece)
    ref_angle = 45
    if is_movement_correct(angle, ref_angle):
        print("Hareket doğru!")
    else:
        print("Hareket yanlış veya tolerans dışında.") 