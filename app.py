from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
import mediapipe as mp
import pickle
import sklearn

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
    return render_template(
        'alfabet.html',
        title = 'Alfabet A-Z',
        active = 'alfabet'
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
    return render_template(
        'kuis-pilihan-ganda.html',
        title = 'Kuis Pilihan Ganda',
        active = 'kuis-pilihan-ganda'
    )
    
@app.route('/kuis-interaktif', endpoint='kuis-interaktif')
def kuis_interaktif():
    return render_template(
        'kuis-interaktif.html',
        title = 'Kuis Interaktif',
        active = 'kuis-interaktif'
    )

@app.route('/skor')
def skor():
    return render_template(
        'skor.html',
        title = 'Skor & Progress',
        active = 'skor'
    )
    
@app.route('/kamus-isyarat', endpoint='kamus-isyarat')
def kamus_isyarat():
    return render_template(
        'kamus-isyarat.html',
        title = 'Kamus Isyarat',
        active = 'kamus-isyarat'
    )

@app.route('/tentang')
def tentang():
    return render_template(
        'tentang.html',
        title = 'Tentang',
        active = 'tentang'
    )
    
@app.route('/saran-masukan', endpoint='saran-masukan')
def saran_masukan():
    return render_template(
        'saran-masukan.html',
        title = 'Saran & Masukan',
        active = 'saran-masukan'
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

        return jsonify({'prediction': predicted_character})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)