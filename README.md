# 🎭 Mask Detector - Panduan Instalasi

Panduan lengkap untuk menginstall dan menjalankan aplikasi **Mask Detector Web Application**.

## 📋 Persyaratan Sistem

### **Minimum Requirements:**

- **Python:** 3.7 atau lebih baru
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 2GB free space
- **Webcam:** Built-in atau external webcam
- **OS:** Windows 10/11, macOS, atau Linux

### **Browser Support:**

- Chrome 80+ (Recommended)
- Firefox 75+
- Edge 80+
- Safari 13+

## 🚀 Instalasi

### **Step 1: Install Python Dependencies**

```bash
# Install semua dependencies yang diperlukan
pip install -r requirements.txt
```

**Dependencies yang akan diinstall:**

- `Flask` - Web framework
- `opencv-python` - Computer vision
- `scikit-learn` - Machine learning
- `joblib` - Model serialization
- `numpy` - Array processing
- `flask-socketio` - Real-time communication
- `eventlet` - Async server

### **Step 2: Persiapan Model**

**Jika model belum ada (`mask_detector_svm.pkl`):**

1. **Siapkan Dataset:**

   - Buat folder `dataset/` di root project
   - Buat subfolder `dataset/with_mask/` dan `dataset/without_mask/`
   - Masukkan gambar training ke folder yang sesuai
   - dataset dapat diakses di https://drive.google.com/file/d/191ugrhUoIAuN3Q6To4goadPMIgQMzt0U/view?usp=sharing

2. **Train Model:**

   ```bash
   python train_mask_detector.py
   ```

   **Output yang diharapkan:**

   ```
   Mulai load dataset...
   Jumlah gambar with_mask: [jumlah]
   Jumlah gambar without_mask: [jumlah]
   ...
   Akurasi model: [XX.XX]%
   Selesai menyimpan model.
   ```

## ▶️ Menjalankan Aplikasi

### **Jalankan Web Application:**

```bash
python app.py
```

**Output yang diharapkan:**

```
🎭 Mask Detector Web Application
📱 Akses aplikasi di: http://localhost:5000
🔍 Sistem deteksi masker real-time
 * Running on http://127.0.0.1:5000
```

### **Akses Aplikasi:**

1. Buka browser
2. Kunjungi: **http://localhost:5000**
3. Klik "Mulai Deteksi"
4. Izinkan akses webcam jika diminta
5. Lihat hasil deteksi real-time

## 🎮 Cara Penggunaan

### **Interface Aplikasi:**

1. **Status Panel:**

   - 🟢 Hijau: Terhubung dan siap
   - 🔴 Merah: Terputus atau error
   - 🟡 Kuning: Sedang mendeteksi

2. **Video Container:**

   - Menampilkan feed webcam real-time
   - Overlay statistik di pojok kanan atas
   - Bounding box: Hijau (dengan masker), Merah (tanpa masker)

3. **Control Panel:**

   - **Mulai Deteksi:** Memulai deteksi masker
   - **Hentikan Deteksi:** Menghentikan deteksi

4. **Informasi Sistem:**
   - Model: Support Vector Machine (SVM)
   - Deteksi: Real-time menggunakan Haar Cascade
   - Input: Webcam 640x480
   - Klasifikasi: Dengan Masker / Tanpa Masker

### **Tips Penggunaan:**

- **Pencahayaan:** Pastikan pencahayaan cukup terang
- **Jarak:** Posisi wajah 50-100cm dari webcam
- **Angle:** Hadapkan wajah langsung ke kamera
- **Background:** Hindari background yang terlalu ramai

## 🔧 Troubleshooting

### **Problem: Model tidak ditemukan**

```
❌ Error: File mask_detector_svm.pkl tidak ditemukan!
```

**Solusi:**

```bash
python train_mask_detector.py
```

### **Problem: Webcam tidak terdeteksi**

```
Error: Tidak dapat mengakses webcam
```

**Solusi:**

1. Pastikan webcam terhubung
2. Tutup aplikasi lain yang menggunakan webcam
3. Restart browser dan aplikasi
4. Check webcam permissions

### **Problem: Dependencies error**

```
ModuleNotFoundError: No module named 'cv2'
```

**Solusi:**

```bash
pip install -r requirements.txt --force-reinstall
```

### **Problem: Port sudah digunakan**

```
Address already in use
```

**Solusi:**

1. Tutup aplikasi yang menggunakan port 5000
2. Atau edit `app.py` untuk menggunakan port lain:
   ```python
   socketio.run(app, port=5001)  # Ganti ke port 5001
   ```

### **Problem: Browser tidak support**

**Solusi:**

- Update browser ke versi terbaru
- Gunakan Chrome atau Firefox
- Enable camera permissions

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Jika belum ada model, train terlebih dahulu
python train_mask_detector.py

# 3. Jalankan aplikasi
python app.py

# 4. Buka browser: http://localhost:5000
```

## 📞 Support

**Jika mengalami masalah:**

1. **Check Requirements:** Pastikan Python 3.7+ dan webcam tersedia
2. **Check Dependencies:** Jalankan `pip install -r requirements.txt`
3. **Check Model:** Pastikan file `mask_detector_svm.pkl` ada
4. **Check Webcam:** Test webcam di aplikasi lain
5. **Check Browser:** Gunakan Chrome/Firefox terbaru
