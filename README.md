# OptiWare MARL: Intelligent Robot Optimization Platform

OptiWare MARL adalah platform analitik cerdas dan simulasi bisnis berbasis kecerdasan buatan (*Multi-Agent Reinforcement Learning*) yang dirancang untuk mengoptimalkan operasional dan pemeliharaan armada robot di gudang pintar (*Smart Warehouse*). 

Proyek ini mencakup seluruh siklus data science, mulai dari pembersihan data, analisis eksploratif (EDA), pemodelan keputusan agen RL menggunakan *Gymnasium*, hingga estimasi finansial ROI proyek dan visualisasi portal web interaktif berbasis Django.

---

## 🌟 Fitur Utama Portal Web

### 1. Dashboard Ringkasan Operasional
![Dashboard Ringkasan Operasional](docs/screenshots/dashboard_ringkasan.png)

Menampilkan metrik utama armada seperti total robot yang terdaftar, jumlah armada aktif (beroperasi), serta estimasi total biaya servis pemeliharaan. Dashboard ini juga memuat status alarm sensor IoT secara real-time (seperti tingkat percepatan dan getaran kritis), serta panel visualisasi interaktif 3D untuk memetakan jam sibuk zona, korelasi downtime, perilaku robot, dan evaluasi model RL.

### 2. Manajemen Armada Robot
![Manajemen Armada Robot](docs/screenshots/armada_robot.png)

Menyajikan tabel komprehensif untuk memantau status operasional setiap robot di dalam gudang secara detail. Pengguna dapat melacak Robot ID, Model, Pabrikan, Status terkini (Active, Idle, Maintenance), jam terbang (operasional), hingga batas kecepatan dan beban maksimal. Dilengkapi dengan filter pencarian untuk menemukan robot secara spesifik.

### 3. Simulasi ROI & Kelayakan Investasi
![Simulasi ROI & Kelayakan Investasi](docs/screenshots/simulasi_roi.png)

Fitur kalkulator interaktif yang memfasilitasi pengguna untuk mensimulasikan penghematan finansial dan ROI (Return on Investment) dari integrasi agen AI/RL. Manajer dapat memodifikasi parameter finansial seperti ukuran armada, biaya investasi awal (CapEx), biaya operasional tahunan (OpEx), biaya kerugian tak langsung per kerusakan, dan baseline kerusakan per tahun untuk melihat analisis kelayakan secara otomatis dan *real-time*.

### 4. Warehouse AI Copilot
![Warehouse AI Copilot](docs/screenshots/warehouse_ai_copilot.png)

Asisten pintar (chatbot) terintegrasi yang membantu manajer gudang mendapatkan wawasan operasional langsung dari basis data tanpa melakukan kueri manual. AI Copilot mampu merespons pertanyaan bahasa alami seperti "berapa jumlah robot tak aktif?" atau "tampilkan alarm sensor terbaru" dan segera menyajikan data yang akurat terkait performa maupun kerusakan armada robot.

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
