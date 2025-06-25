# data/raw/ klasörü

Bu klasörde, egzersiz hareketlerine ait anahtar nokta (keypoint) verileri ve ham veri setleri bulunur.

## Önerilen Dosya Yapısı
- biceps_curl_keypoints.csv
- pushup_keypoints.csv
- (veya) RiccardoRiccio/Fitness-AI-Trainer-With-Automatic-Exercise-Recognition-and-Counting projesinden alınan .csv/.npz/.json dosyaları

## Açıklama
- Her dosya, frame/frame anahtar noktalarını ve egzersiz etiketini içermelidir.
- Örnek kolonlar: `frame_id, joint_0_x, joint_0_y, ..., joint_32_x, joint_32_y, exercise_label`

## Kaynaklar
- [Fitness-AI-Trainer-With-Automatic-Exercise-Recognition-and-Counting](https://github.com/RiccardoRiccio/Fitness-AI-Trainer-With-Automatic-Exercise-Recognition-and-Counting)
- Kendi oluşturduğunuz veya topladığınız keypoint verileri 