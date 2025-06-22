import glob
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import time  # untuk menghitung waktu

IMG_SIZE = 100

data = []
labels = []

print("Mulai load dataset...")

start_load = time.time()

with_mask_files = glob.glob('dataset/with_mask/*.jpg')
without_mask_files = glob.glob('dataset/without_mask/*.jpg')

print(f"Jumlah gambar with_mask: {len(with_mask_files)}")
print(f"Jumlah gambar without_mask: {len(without_mask_files)}")

for i, img_path in enumerate(with_mask_files):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Gagal membaca {img_path}")
        continue
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    data.append(img.flatten())
    labels.append(0)
    if i % 100 == 0:
        print(f"Memproses gambar with_mask ke-{i}")

for i, img_path in enumerate(without_mask_files):
    img = cv2.imread(img_path)
    if img is None:
        print(f"Gagal membaca {img_path}")
        continue
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    data.append(img.flatten())
    labels.append(1)
    if i % 100 == 0:
        print(f"Memproses gambar without_mask ke-{i}")

end_load = time.time()
print(f"Selesai load dataset dalam {end_load - start_load:.2f} detik")

print("Memulai split dataset...")
start_split = time.time()
data = np.array(data)
labels = np.array(labels)

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)

end_split = time.time()
print(f"Selesai split dataset dalam {end_split - start_split:.2f} detik")

print("Mulai training model SVM...")
start_train = time.time()

model = SVC(kernel='linear')
model.fit(X_train, y_train)

end_train = time.time()
print(f"Selesai training dalam {end_train - start_train:.2f} detik")

print("Mulai evaluasi model...")
start_eval = time.time()

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

end_eval = time.time()
print(f"Selesai evaluasi dalam {end_eval - start_eval:.2f} detik")
print(f"Akurasi model: {accuracy * 100:.2f}%")

print("Menyimpan model ke file mask_detector_svm.pkl")
joblib.dump(model, 'mask_detector_svm.pkl')
print("Selesai menyimpan model.")
