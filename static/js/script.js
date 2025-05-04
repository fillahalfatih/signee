let video = document.getElementById("webcam");
let startButton = document.getElementById("start-camera");
let stopButton = document.getElementById("stop-camera");
let captureButton = document.getElementById("capture");
let stream = null;

// Fungsi untuk mengaktifkan kamera
startButton.addEventListener("click", function () {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (mediaStream) {
            stream = mediaStream;
            video.srcObject = mediaStream;
            video.style.display = "block";  // Tampilkan video
            startButton.disabled = true;
            stopButton.disabled = false;
            captureButton.disabled = false;
        })
        .catch(function (err) {
            console.error("Gagal mengakses webcam: ", err);
        });
});

// Fungsi untuk mematikan kamera
stopButton.addEventListener("click", function () {
    if (stream) {
        let tracks = stream.getTracks();
        tracks.forEach(track => track.stop());  // Hentikan semua track media
        video.srcObject = null;
        video.style.display = "none";  // Sembunyikan video
        startButton.disabled = false;
        stopButton.disabled = true;
        captureButton.disabled = true;
    }
});

// Fungsi menangkap gambar dari webcam
function capture() {
    let canvas = document.getElementById("canvas");
    let context = canvas.getContext("2d");

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Mengonversi gambar menjadi base64
    let imageData = canvas.toDataURL("image/png");

    // Kirim ke server Flask untuk prediksi
    fetch('/predict', {
        method: 'POST',
        body: JSON.stringify({ image: imageData }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction) {
            document.getElementById("prediction-result").innerText = "Prediksi: " + data.prediction;

            // Perbarui elemen prediction-accuracy jika akurasi tersedia
            if (data.accuracy !== null && !isNaN(data.accuracy)) {
                document.getElementById("prediction-accuracy").innerText = (data.accuracy * 100).toFixed(2) + "%";
            } else {
                document.getElementById("prediction-accuracy").innerText = "Akurasi tidak tersedia";
            }
        } else {
            document.getElementById("prediction-result").innerText = "Error: " + (data.error || "Gagal memproses");
            document.getElementById("prediction-accuracy").innerText = ""; // Kosongkan akurasi jika terjadi error
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("prediction-result").innerText = "Error: Gagal mengirim data";
        document.getElementById("prediction-accuracy").innerText = ""; // Kosongkan akurasi jika terjadi error
    });
}

const startBtn = document.getElementById('start-camera');
const stopBtn = document.getElementById('stop-camera');
const webcam = document.getElementById('webcam');
const previewImg = document.getElementById('preview-image');

startBtn.addEventListener('click', function() {
    previewImg.style.display = 'none';
    webcam.style.display = '';
});

stopBtn.addEventListener('click', function() {
    previewImg.style.display = '';
    webcam.style.display = 'none';
});

function startCountdown() {
    const captureBtn = document.getElementById('capture');
    let seconds = 3;
    const originalText = 'Ambil Gambar';
    captureBtn.disabled = true;
    captureBtn.textContent = seconds;

    const interval = setInterval(() => {
        seconds--;
        if (seconds > 0) {
            captureBtn.textContent = seconds;
        } else {
            clearInterval(interval);
            captureBtn.textContent = originalText;
            captureBtn.disabled = false;
            capture();
        }
    }, 1000);
}
