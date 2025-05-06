from flask import Flask, render_template, request, jsonify, abort
import base64
import cv2
import numpy as np
import mediapipe as mp
import pickle
import sklearn
import json
import os

app = Flask(__name__)

# Load model dari file .p
model_dict = pickle.load(open('model/rf_model.p', 'rb'))
model = model_dict['model']

# Definisikan labels_dict untuk mapping label numerik ke huruf
class_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
labels_dict = {i: class_labels[i] for i in range(len(class_labels))}

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title = 'Beranda',
        active = 'beranda')

@app.route('/pengantar')
def pengantar():
    return render_template(
        'pengantar.html',
        title = 'Pengantar',
        active = 'pengantar'
    )
    
@app.route('/alfabet')
def alfabet():
    try:
        with open('data-alfabet.json') as f:
            alfabet = json.load(f)
    except FileNotFoundError:
        alfabet = "Alfabet data not found"

    return render_template(
        'alfabet.html',
        title = 'Alfabet A-Z',
        active = 'alfabet',
        alfabet = alfabet
    )
    
@app.route('/tips-trik', endpoint='tips-trik')
def tips_trik():
    return render_template(
        'tips-trik.html',
        title = 'Tips & Trik',
        active = 'tips-trik'
    )

@app.route('/kuis-pilihan-ganda', endpoint='kuis-pilihan-ganda')
def kuis_pilihan_ganda():
    try:
        with open('data-pg.json') as f:
            kuis_data = json.load(f)
        total_soal = len(kuis_data)
    except FileNotFoundError:
        total_soal = 0

    return render_template(
        'kuis-pilihan-ganda-onboarding.html',
        title = 'Kuis Pilihan Ganda',
        active = 'kuis-pilihan-ganda',
        total_soal = total_soal
    )
    
# Route untuk tiap kuis berdasarkan id
@app.route('/kuis-pilihan-ganda/<int:kuis_id>')
def kuis_pilihan_ganda_detail(kuis_id):
    # Load data dari JSON
    try:
        with open('data-pg.json') as f:
            kuis_data = json.load(f)
    except FileNotFoundError:
        abort(404, description="Data tidak ditemukan")
    
    # Cari kuis berdasarkan id
    kuis = next((item for item in kuis_data if item["id"] == kuis_id), None)
    
    if kuis is None:
        abort(404, description="Kuis tidak ditemukan")
    
    return render_template(
        'kuis-pilihan-ganda.html',
        title = f'Kuis Pilihan Ganda',
        active = 'kuis-pilihan-ganda',
        kuis = kuis,
        total_soal = len(kuis_data)  # Kirim total jumlah soal ke template
    )
    
@app.route('/kuis-interaktif', endpoint='kuis-interaktif')
def kuis_interaktif():
    try:
        with open('data-interaktif.json') as f:
            kuis_data = json.load(f)
        total_soal = len(kuis_data)
    except FileNotFoundError:
        total_soal = 0

    return render_template(
        'kuis-interaktif-onboarding.html',
        title = 'Kuis Interaktif',
        active = 'kuis-interaktif',
        total_soal = total_soal
    )

# Route untuk tiap kuis berdasarkan id
@app.route('/kuis-interaktif/<int:kuis_id>')
def kuis_interaktif_detail(kuis_id):
    # Load data dari JSON
    try:
        with open('data-interaktif.json') as f:
            kuis_data = json.load(f)
    except FileNotFoundError:
        abort(404, description="Data tidak ditemukan")
    
    # Cari kuis berdasarkan id
    kuis = next((item for item in kuis_data if item["id"] == kuis_id), None)
    
    if kuis is None:
        abort(404, description="Kuis tidak ditemukan")
    
    return render_template(
        'kuis-interaktif.html',
        title = f'Kuis Interaktif',
        active = 'kuis-interaktif',
        kuis = kuis,
        total_soal = len(kuis_data)  # Kirim total jumlah soal ke template
    )

@app.route('/skor')
def skor():
    # Baca data dari file JSON
    try:
        with open('data-pg-jawaban.json') as f:
            data_pg_jawaban = json.load(f)
    except FileNotFoundError:
        data_pg_jawaban = []

    try:
        with open('data-interaktif-jawaban.json') as f:
            data_interaktif_jawaban = json.load(f)
    except FileNotFoundError:
        data_interaktif_jawaban = []

    # Kirim data ke template
    # Sorting berdasarkan id secara ascending (ASC)
    data_pg_jawaban = sorted(data_pg_jawaban, key=lambda x: x.get('id', 0))
    data_interaktif_jawaban = sorted(data_interaktif_jawaban, key=lambda x: x.get('id', 0))

    return render_template(
        'skor.html',
        title = 'Skor & Progress',
        active = 'skor',
        data_pg_jawaban = data_pg_jawaban,
        data_interaktif_jawaban = data_interaktif_jawaban,
    )

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]  # Menghapus header base64
        image_bytes = base64.b64decode(image_data)

        # Konversi ke format OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Proses gambar dengan MediaPipe untuk mendeteksi tangan
        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return jsonify({'error': 'Tidak ada tangan terdeteksi'}), 400

        data_aux = []
        x_ = []
        y_ = []

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # Prediksi menggunakan model
        prediction = model.predict([np.asarray(data_aux)])

        # Konversi hasil prediksi ke huruf
        predicted_character = labels_dict[int(prediction[0])] if isinstance(prediction[0], (int, np.integer)) else prediction[0]

        # Dapatkan probabilitas prediksi jika model mendukung predict_proba
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba([np.asarray(data_aux)])
            accuracy = float(np.max(proba))  # Probabilitas tertinggi
        else:
            accuracy = 1.0  # Asumsikan prediksi 100% jika tidak tersedia proba

        return jsonify({'prediction': predicted_character, 'accuracy': accuracy})
        # return jsonify({'prediction': predicted_character})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit-jawaban-pg', methods=['POST'])
def submit_jawaban():
    data = request.get_json()
    jawaban_baru = {
        "id": data['id'],
        "opsi_dipilih": data['opsi_dipilih'],
        "jawaban_benar": data['jawaban_benar'],
        "gambar_soal": data['gambar_soal'],
        "isTrue": 1 if data['opsi_dipilih'] == data['jawaban_benar'] else 0
    }

    path = 'data-pg-jawaban.json'

    # Cek kalau file belum ada
    if not os.path.exists(path):
        jawaban_list = []
    else:
        with open(path, 'r') as f:
            try:
                jawaban_list = json.load(f)
            except json.JSONDecodeError:
                jawaban_list = []

    # Hapus jawaban lama jika udah ada id yang sama (overwrite)
    jawaban_list = [j for j in jawaban_list if j['id'] != data['id']]
    jawaban_list.append(jawaban_baru)

    # Simpan kembali
    with open(path, 'w') as f:
        json.dump(jawaban_list, f, indent=4)

    return jsonify({'status': 'ok'})

@app.route('/submit-jawaban-interaktif', methods=['POST'])
def submit_jawaban_interaktif():
    try:
        data = request.get_json()
        jawaban_baru = {
            "id": data['id'],
            "soal": data['soal'],
            "soal_huruf": data['soal_huruf'],
            "jawaban": data['jawaban'],
            "isTrue": data['isTrue']
        }

        path = 'data-interaktif-jawaban.json'

        # Cek jika file belum ada
        if not os.path.exists(path):
            jawaban_list = []
        else:
            with open(path, 'r') as f:
                try:
                    jawaban_list = json.load(f)
                except json.JSONDecodeError:
                    jawaban_list = []

        # Hapus jawaban lama jika sudah ada id yang sama (overwrite)
        jawaban_list = [j for j in jawaban_list if j['id'] != data['id']]
        jawaban_list.append(jawaban_baru)

        # Simpan kembali ke file
        with open(path, 'w') as f:
            json.dump(jawaban_list, f, indent=4)

        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)