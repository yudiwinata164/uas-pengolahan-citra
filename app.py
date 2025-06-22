from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import joblib
import base64
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mask_detector_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Load model dan face cascade untuk deteksi masker
model = joblib.load('mask_detector_svm.pkl')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

IMG_SIZE = 100  # Ukuran gambar untuk preprocessing

class MaskDetector:
    def __init__(self):
        self.is_detecting = False
        self.cap = None
        
    def start_detection(self):
        """Mulai deteksi masker real-time menggunakan webcam"""
        if self.is_detecting:
            return
            
        self.is_detecting = True
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("Error: Tidak dapat mengakses webcam")
            self.is_detecting = False
            return
            
        # Thread untuk processing video
        detection_thread = threading.Thread(target=self._detection_loop)
        detection_thread.daemon = True
        detection_thread.start()
        
    def stop_detection(self):
        """Stop deteksi"""
        self.is_detecting = False
        if self.cap:
            self.cap.release()
            
    def _detection_loop(self):
        """Loop deteksi masker real-time"""
        while self.is_detecting:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Deteksi wajah menggunakan Haar Cascade
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

            detection_results = []

            for (x, y, w, h) in faces:
                # Ekstrak dan preprocess wajah
                face = frame[y:y+h, x:x+w]
                face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
                face_flat = face_resized.flatten().reshape(1, -1)

                # Prediksi menggunakan model SVM
                label = model.predict(face_flat)[0]
                label_text = "Mask" if label == 0 else "No Mask"
                color = (0, 255, 0) if label == 0 else (0, 0, 255)

                # Gambar bounding box dan label
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                # Simpan hasil deteksi untuk dikirim ke frontend
                detection_results.append({
                    'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h),
                    'label': label_text,
                    'color': color,
                    'confidence': float(label)
                })
            
            # Encode frame untuk dikirim ke browser
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
            
            # Kirim data ke frontend via WebSocket
            socketio.emit('video_frame', {
                'image': frame_data,
                'detections': detection_results,
                'timestamp': time.time()
            })
            
            time.sleep(0.033)  # ~30 FPS
            
        if self.cap:
            self.cap.release()

# Instance detector
detector = MaskDetector()

@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')

@socketio.on('start_detection')
def handle_start_detection():
    """Handle request untuk mulai deteksi"""
    print("Memulai deteksi masker...")
    detector.start_detection()
    emit('detection_status', {'status': 'started', 'message': 'Deteksi masker dimulai'})

@socketio.on('stop_detection')
def handle_stop_detection():
    """Handle request untuk stop deteksi"""
    print("Menghentikan deteksi masker...")
    detector.stop_detection()
    emit('detection_status', {'status': 'stopped', 'message': 'Deteksi masker dihentikan'})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client terhubung')
    emit('connection_status', {'status': 'connected', 'message': 'Terhubung ke server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client terputus')
    detector.stop_detection()

if __name__ == '__main__':
    print("🎭 Mask Detector Web Application")
    print("📱 Akses aplikasi di: http://localhost:5000")
    print("🔍 Sistem deteksi masker real-time")
    socketio.run(app, debug=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
