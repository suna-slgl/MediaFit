import sys
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from angle_analysis import calculate_angle, is_movement_correct

# Dracula Tema Renkleri
DRACULA_COLORS = {
    'bg': '#3a3d4a',           # Ana arka plan 
    'fg': '#f8f8f2',           # Ana metin
    'comment': '#a9b4d5',      # Yorum rengi
    'cyan': '#cff993',         # Cyan
    'green': '#93f9bd',        # Yeşil
    'orange': '#f9bd93',       # Turuncu
    'pink': '#CC609E',         # Pembe
    'purple': '#bd93f9',       # Mor
    'red': '#ff5555',          # Kırmızı
    'yellow': '#f1fa8c',       # Sarı
    'selection': '#44475a',    # Seçim arka planı
    'current_line': '#44475a', # Mevcut satır
    'button_bg': '#44475a',    # Buton arka planı
    'button_fg': '#f9bd93',    # Buton metin
    'button_hover': '#6272a4', # Buton hover
    'frame_bg': '#44475a',     # Frame arka planı
    'border': '#6272a4'        # Kenarlık
}

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

class ModernButton(tk.Button):
    """Modern görünümlü buton sınıfı"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=DRACULA_COLORS['button_bg'],
            fg=DRACULA_COLORS['button_fg'],
            activebackground=DRACULA_COLORS['button_hover'],
            activeforeground=DRACULA_COLORS['button_fg'],
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=8,
            font=('Roboto', 10, 'bold'),
            cursor='hand2'
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
    
    def on_enter(self, e):
        self.configure(bg=DRACULA_COLORS['button_hover'])
    
    def on_leave(self, e):
        self.configure(bg=DRACULA_COLORS['button_bg'])

class CameraThread(threading.Thread):
    def __init__(self, exercise_name, callback_image, callback_angle):
        super().__init__()
        self._run_flag = True
        self.exercise_name = exercise_name
        self.callback_image = callback_image
        self.callback_angle = callback_angle
        self.cap = None

    def run(self):
        mp_pose = mp.solutions.pose
        self.cap = cv2.VideoCapture(0)
        
        # Kamera açılamazsa thread'i sonlandır
        if not self.cap.isOpened():
            print("Kamera açılamadı!")
            return
            
        config = EXERCISE_CONFIG[self.exercise_name]
        joints = config['joints']
        ref_angle = config['ref_angle']
        tolerance = config['tolerance']
        
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self._run_flag:
                ret, frame = self.cap.read()
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
                    self.callback_angle(angle, correct)
                except Exception:
                    self.callback_angle(-1, False)
                
                # Anahtar noktaları çiz
                if results.pose_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                
                # Görüntüyü Tkinter formatına çevir
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.callback_image(rgb_image)
                
                time.sleep(0.015)  # ~66 FPS
                
        self.release_camera()

    def stop(self):
        self._run_flag = False
        
    def release_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MediaFit")
        self.root.geometry("500x900") 
        
        # Dracula temasını uygula
        self.apply_dracula_theme()
        
        # Thread değişkeni
        self.thread = None
        self.is_running = False
        
        # GUI bileşenlerini oluştur
        self.create_widgets()
        
        # Pencere kapatıldığında thread'i durdur
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ctrl+C ile kapatma
        self.root.bind('<Control-c>', self.on_closing)

    def apply_dracula_theme(self):
        """Dracula temasını uygula"""
        self.root.configure(bg=DRACULA_COLORS['bg'])
        
        # Style yapılandırması
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame style
        style.configure('Dracula.TFrame', background=DRACULA_COLORS['bg'])
        style.configure('Card.TFrame', background=DRACULA_COLORS['frame_bg'], relief='flat')
        
        # Label style
        style.configure('Dracula.TLabel', 
                       background=DRACULA_COLORS['bg'], 
                       foreground=DRACULA_COLORS['fg'],
                       font=('Roboto', 10))
        
        style.configure('Title.TLabel', 
                       background=DRACULA_COLORS['bg'], 
                       foreground=DRACULA_COLORS['cyan'],
                       font=('Roboto', 16, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       background=DRACULA_COLORS['bg'], 
                       foreground=DRACULA_COLORS['purple'],
                       font=('Roboto', 12))
        
        # Combobox style
        style.configure('Dracula.TCombobox', 
                       fieldbackground=DRACULA_COLORS['frame_bg'],
                       background=DRACULA_COLORS['frame_bg'],
                       foreground=DRACULA_COLORS['fg'],
                       arrowcolor=DRACULA_COLORS['cyan'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Dracula.TCombobox',
                 fieldbackground=[('readonly', DRACULA_COLORS['frame_bg'])],
                 selectbackground=[('readonly', DRACULA_COLORS['selection'])],
                 selectforeground=[('readonly', DRACULA_COLORS['fg'])])

    def create_widgets(self):
        # Ana frame
        main_frame = ttk.Frame(self.root, style='Dracula.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlıklarını ayarla - Sadece kamera satırı genişlesin
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Sadece kamera satırı (row=2) genişlesin
        
        # Başlık
        title_label = ttk.Label(main_frame, text="MediaFit", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Egzersiz seçici kartı
        exercise_frame = ttk.Frame(main_frame, style='Dracula.TFrame', padding="15")
        exercise_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        exercise_frame.columnconfigure(1, weight=1)
        
        ttk.Label(exercise_frame, text="Egzersiz Seçin:", style='Subtitle.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        self.exercise_var = tk.StringVar()
        self.exercise_combo = ttk.Combobox(exercise_frame, textvariable=self.exercise_var, 
                                          values=list(EXERCISE_CONFIG.keys()), 
                                          state="readonly", style='Dracula.TCombobox',
                                          font=('Roboto', 11))
        self.exercise_combo.set('Biceps Curl')
        self.exercise_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Kamera görüntüsü kartı - Sabit boyut
        camera_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="10")
        camera_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        camera_frame.columnconfigure(0, weight=1)
        camera_frame.rowconfigure(0, weight=1)
        
        # Kamera frame'ine sabit boyut ver
        camera_frame.configure(width=480, height=365)  # Kamera boyutuna uygun
        
        # Kamera label'ı için sabit boyut - Kamera açılmış haline göre ayarla
        self.camera_label = ttk.Label(camera_frame, text="LIVE CAMERA", 
                                     style='Dracula.TLabel',
                                     font=('Roboto', 12, 'bold'),
                                     anchor='center')
        self.camera_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Kamera label'ına sabit boyut ver (kamera açılmış haline göre)
        self.camera_label.configure(width=60)  # Kamera genişliğine uygun
        
        # Açı bilgisi kartı - Sabit konum
        angle_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        angle_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.angle_label = ttk.Label(angle_frame, text="Açı: -", 
                                   style='Dracula.TLabel',
                                   font=('Roboto', 14, 'bold'))
        self.angle_label.grid(row=0, column=0, sticky=tk.W)
        
        # Butonlar kartı - Sabit konum
        button_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="15")
        button_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Sol butonlar
        left_buttons = ttk.Frame(button_frame, style='Card.TFrame')
        left_buttons.pack(side=tk.LEFT)
        
        self.start_button = ModernButton(left_buttons, text="Başlat", command=self.start_camera)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ModernButton(left_buttons, text="Durdur", command=self.stop_camera, state="disabled")
        self.stop_button.pack(side=tk.LEFT)
        
        # Sağ buton
        self.quit_button = ModernButton(button_frame, text="Çıkış", command=self.on_closing)
        self.quit_button.pack(side=tk.RIGHT)
        
        # Alt bilgi - Sabit konum
        info_label = ttk.Label(main_frame, text="Ctrl+C ile hızlı çıkış yapabilirsiniz", 
                              style='Dracula.TLabel',
                              font=('Roboto', 9))
        info_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    def start_camera(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        exercise = self.exercise_var.get()
        
        self.thread = CameraThread(exercise, self.update_image, self.update_angle)
        self.thread.daemon = True
        self.thread.start()

    def stop_camera(self):
        if not self.is_running:
            return
            
        self.is_running = False
        
        if self.thread:
            self.thread.stop()
            # Thread'in durmasını bekle (maksimum 2 saniye)
            self.thread.join(timeout=2.0)
            if self.thread.is_alive():
                print("Thread durdurulamadı, zorla kapatılıyor...")
            self.thread = None
        
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.camera_label.config(text="LIVE CAMERA", image="", anchor='center')

    def update_image(self, rgb_image):
        if not self.is_running:
            return
            
        try:
            # RGB görüntüyü PIL Image'e çevir
            pil_image = Image.fromarray(rgb_image)
            
            # Daha küçük sabit boyut (pencere genişliğine uygun)
            target_width = 460  # 500 - 40 (padding)
            target_height = 345  # 4:3 oranı
            
            # Görüntüyü sabit boyuta ölçekle
            pil_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # PIL Image'i Tkinter PhotoImage'e çevir
            photo = ImageTk.PhotoImage(pil_image)
            
            # Label'ı güncelle (referansı koru)
            self.camera_label.config(image=photo, text="")
            self.camera_label.image = photo  # Referansı koru
        except Exception as e:
            print(f"Görüntü güncelleme hatası: {e}")

    def update_angle(self, angle, correct):
        if not self.is_running:
            return
            
        try:
            if angle == -1:
                self.angle_label.config(text="Açı: -", foreground=DRACULA_COLORS['comment'])
            else:
                self.angle_label.config(text=f"Açı: {angle:.1f}°", foreground=DRACULA_COLORS['fg'])
        except Exception as e:
            print(f"Açı güncelleme hatası: {e}")

    def on_closing(self, event=None):
        print("Uygulama kapatılıyor...")
        self.stop_camera()
        
        # Tüm widget'ları temizle
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
        
        # Zorla çıkış
        os._exit(0)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nCtrl+C ile kapatıldı")
        os._exit(0)
    except Exception as e:
        print(f"Hata: {e}")
        os._exit(1)