# 🚲 Proyek Analisis Data: Bike Sharing Dataset

Proyek Akhir untuk modul pembelajaran **"Belajar Analisis Data dengan Python"** di Dicoding. Proyek ini mencakup proses data wrangling, exploratory data analysis (EDA), teknik analisis lanjutan (binning/clustering manual), visualisasi data, serta pembuatan dashboard interaktif berbasis **Streamlit**.

---

## 📁 Struktur Direktori
```text
submission/
├── dashboard/
│   ├── main_data.csv        # Dataset bersih siap pakai untuk dashboard
│   └── dashboard.py         # Skrip aplikasi dashboard Streamlit
├── data/
│   ├── day.csv              # Dataset mentah agregasi harian
│   └── hour.csv             # Dataset mentah agregasi per jam
├── notebook.ipynb           # Jupyter notebook berisi seluruh proses analisis data
├── README.md                # Dokumentasi proyek dan panduan menjalankan
├── requirements.txt         # Daftar pustaka (library) yang dibutuhkan
└── url.txt                  # Tautan dashboard yang dideploy di Streamlit Cloud
```

---

## 🎯 Pertanyaan Bisnis (SMART Framework)
1. **Pertanyaan 1 (Dampak Musim & Cuaca):**
   *Bagaimana pengaruh kondisi cuaca dan musim terhadap jumlah rata-rata penyewaan sepeda harian selama periode 2011–2012, dan musim apa yang mencatatkan performa penyewaan tertinggi?*
2. **Pertanyaan 2 (Pola Pengguna Jam Sibuk):**
   *Bagaimana pola perbandingan penyewaan antara pengguna casual dan registered berdasarkan jam dalam sehari (khususnya jam sibuk komuter 07:00–09:00 dan 17:00–19:00) pada hari kerja (working day)?*

---

## 🛠️ Panduan Menjalankan Proyek Secara Lokal

### 1. Prasyarat
Pastikan Anda telah menginstal **Python 3.9** atau versi lebih baru pada perangkat Anda.

### 2. Buat Lingkungan Virtual (Opsional namun Disarankan)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependensi
Pindah ke direktori submission dan instal seluruh pustaka yang diperlukan:
```bash
cd submission
pip install -r requirements.txt
```

### 4. Menjalankan Notebook Analisis
Buka file `notebook.ipynb` menggunakan Jupyter Lab, VS Code, atau Google Colab:
```bash
jupyter notebook notebook.ipynb
```

### 5. Menjalankan Dashboard Streamlit
Untuk menjalankan dashboard interaktif secara lokal, jalankan perintah berikut dari direktori utama atau direktori dashboard:
```bash
cd dashboard
streamlit run dashboard.py
```
Aplikasi dashboard akan terbuka secara otomatis di browser Anda pada alamat default:
`http://localhost:8501`

---

## 📊 Ringkasan Hasil Analisis
- **Musim & Cuaca:** Musim Gugur (*Fall*) membukukan rata-rata sewa tertinggi (~5.644 unit/hari), sedangkan Musim Semi (*Spring*) mencatatkan yang terendah (~2.604 unit/hari). Cuaca cerah mendominasi penggunaan, sementara hujan/salju menurunkan penggunaan secara drastis hingga >60%.
- **Pengguna Komuter vs Santai:** Pada hari kerja, pengguna *registered* melonjak tajam pada jam 08:00 (pagi) dan 17:00–18:00 (sore) dengan proporsi di atas 85–90%, menandakan fungsi utama sepeda sebagai sarana komuter. Pengguna *casual* lebih aktif di akhir pekan antara pukul 12:00–16:00.
- **Teknik Analisis Lanjutan:** Segmentasi waktu (*Time Binning*) dan level permintaan (*Demand Categorization*) membantu tim operasional merancang strategi pemeliharaan armada pada sesi sepi (00:00–05:00) dan redistribusi unit docking menjelang jam sibuk.

