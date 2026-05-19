# OptiWare MARL: Intelligent Robot Optimization Platform

OptiWare MARL adalah platform analitik cerdas dan simulasi bisnis berbasis kecerdasan buatan (*Multi-Agent Reinforcement Learning*) yang dirancang untuk mengoptimalkan operasional dan pemeliharaan armada robot di gudang pintar (*Smart Warehouse*). 

Proyek ini mencakup seluruh siklus data science, mulai dari pembersihan data, analisis eksploratif (EDA), pemodelan keputusan agen RL menggunakan *Gymnasium*, hingga estimasi finansial ROI proyek dan visualisasi portal web interaktif berbasis Django.

---

## 🌟 Fitur Utama Portal Web

1. **Dashboard Ringkasan Operasional**: Menampilkan metrik utama armada (total robot aktif/idle/maintenance), status alarm sensor secara langsung, serta tingkat kepadatan zona gudang.
2. **Visualisasi Interaktif 3D**: Grafik 3D berbasis *Plotly.js* yang memetakan jam sibuk per zona, korelasi durasi downtime perbaikan, perilaku termal baterai robot, serta visualisasi kurva konvergensi Q-Table agen RL.
3. **Simulator Kelayakan ROI Interaktif**: Kalkulator kelayakan investasi proyek dengan parameter masukan yang dapat disesuaikan (CapEx, OpEx, ukuran armada, biaya kerusakan). Menghitung metrik finansial seperti **NPV, IRR (menggunakan solver Newton-Raphson), Payback Period, dan ROI 3-Tahun** secara *real-time*.
4. **Warehouse AI Copilot**: Asisten pintar berbasis teks yang terintegrasi secara langsung dengan basis data SQLite untuk menjawab pertanyaan terkait kondisi gudang dan armada robot saat ini secara dinamis.

---

## 📂 Struktur Direktori

```text
├── cleaned_data/              # Dataset bersih hasil preprocessing (.csv)
├── docs/                      # Dokumen proposal proyek & plot visualisasi
├── warehouse_portal/          # Direktori proyek utama Django
├── dashboard/                 # Aplikasi portal web (model, views, templates)
│   ├── management/commands/   # Perintah kustom pengunggah data ke database
│   ├── static/                # Aset gambar statis pendukung
│   └── templates/             # Tampilan dashboard, simulasi, dan AI Copilot
├── 01_Data_Cleaning_Preprocessing.ipynb  # Notebook Integrasi & Pembersihan Data
├── 02_Exploratory_Data_Analysis.ipynb     # Notebook Visualisasi Analisis Pola Gudang
├── 03_RL_Modeling_Maintenance.ipynb      # Notebook Pemodelan Agen RL (Q-Learning)
├── 04_Business_ROI_Simulation.ipynb      # Notebook Analisis Keuangan & Simulasi ROI
├── .gitignore                 # Daftar pengabaian berkas Git
├── requirements.txt           # Daftar dependensi modul Python
└── README.md                  # Dokumentasi proyek (berkas ini)
```

---

## 🚀 Panduan Langkah Menjalankan Proyek

### 1. Instalasi Dependensi
Pastikan Python 3.10+ telah terinstal, lalu pasang pustaka-pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

### 2. Migrasi Database Django
Siapkan skema database SQLite lokal Anda dengan menjalankan migrasi:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Memuat Data CSV ke SQLite (Seeding)
Gunakan perintah kustom Django untuk memuat data dari folder `cleaned_data/` ke database SQLite secara otomatis:
```bash
python manage.py load_cleaned_data
```

### 4. Menjalankan Server Web Django
Mulai server pengembang Django lokal:
```bash
python manage.py runserver
```

Buka peramban (browser) Anda dan akses alamat berikut untuk mencoba portal:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Alur Pemodelan Data Science (Jupyter Notebooks)

1. **`01_Data_Cleaning_Preprocessing.ipynb`**
   * Menyelesaikan masalah inkonsistensi kunci referensi (*disjoint keys*) antara tabel fakta dan dimensi.
   * Mencapai 100% *match rate* untuk ID Robot dan ID Zona sebelum memasuki tahap analisis.
2. **`02_Exploratory_Data_Analysis.ipynb`**
   * Mengidentifikasi jam sibuk lalu lintas gudang (puncak aktivitas pukul 08:00 - 10:00 dan 16:00 - 18:00).
   * Menganalisis korelasi downtime perbaikan mekanik serta perilaku termal baterai robot terhadap berat muatan.
3. **`03_RL_Modeling_Maintenance.ipynb`**
   * Membuat lingkungan kustom *Gymnasium* dengan pemodelan degradasi keausan berbasis distribusi Weibull.
   * Melatih agen *Tabular Q-Learning* untuk menjadwalkan servis preventif secara optimal, menekan tingkat breakdown darurat tahunan hingga **0 kali** (dibandingkan heuristik dasar).
4. **`04_Business_ROI_Simulation.ipynb`**
   * Memodelkan kelayakan finansial penerapan kebijakan RL selama 3 tahun untuk 300 robot.
   * Membuktikan potensi penghematan tahunan sebesar **$1.39M USD** dengan Payback Period **4.5 bulan** dan 3-Year ROI sebesar **704.9%**.
