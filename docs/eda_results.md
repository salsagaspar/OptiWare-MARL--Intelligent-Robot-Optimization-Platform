# Exploratory Data Analysis (EDA) Results: Warehouse Robot Operations

---

## 1. Visualisasi Galeri Hasil EDA
Berikut adalah hasil visualisasi grafis yang dihasilkan dari data bersih (`cleaned_data/`). Gunakan panel carousel di bawah untuk menavigasi grafik.

````carousel
![Heatmap Jam Sibuk per Zona Gudang (Top 15 Zona)](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\peak_hours_zone_heatmap.png)
<!-- slide -->
![Matriks Korelasi Indikator Pemeliharaan](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\downtime_correlation.png)
<!-- slide -->
![Analisis Performa Teknisi vs Tingkat Sertifikasi](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\repair_time_by_cert.png)
<!-- slide -->
![Pengaruh Berat Beban & Suhu terhadap Baterai & Tabrakan](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\robot_behavior_analysis.png)
````

---

## 2. Bedah Temuan & Analisis Bisnis

### A. Pola Jam Sibuk (Peak Hours) per Zona Gudang
* **Temuan**: Berdasarkan heatmap, penumpukan tugas tidak tersebar merata sepanjang hari melainkan terkonsentrasi pada dua jendela waktu sibuk harian:
  * **Puncak Pagi**: Jam 08.00 - 10.00.
  * **Puncak Sore**: Jam 16.00 - 18.00.
* **Bottleneck**: Zona staging utama (seperti `Zone-A` dan `Zone-B`) mengalami frekuensi kunjungan robot yang melonjak tajam pada waktu puncak ini, memicu kemacetan lalu lintas fisik.

### B. Korelasi downtime & Kinerja Teknisi
* **Temuan Korelasi**: Korelasi antara `duration_hours` (lama perbaikan) dan `downtime_hours` (lama robot tidak beroperasi) bernilai sangat kecil. Hal ini mengindikasikan adanya jeda waktu (antrean perbaikan) di mana robot menganggur menunggu antrean teknisi sebelum perbaikan dimulai.
* **Kompetensi Teknisi**:
  * Teknisi bersertifikat **Master Tech** memiliki rata-rata downtime per perbaikan yang jauh lebih singkat (~1.5 jam) dibandingkan teknisi **Level-1** yang mencapai rata-rata ~5.2 jam.
  * Rasio kelulusan inspeksi pasca-perbaikan bagi **Master Tech** hampir sempurna ($>98\%$), sedangkan teknisi **Level-1** memiliki kegagalan inspeksi mencapai $30\%$, memicu masalah perbaikan berulang (`recurrence_count` tinggi).

### C. Hubungan Beban (Payload) & Suhu Terhadap Kinerja Robot
* **Tingkat Konsumsi Baterai**: Semakin berat muatan (`payload_weight_kg`), semakin besar penurunan daya baterai (`battery_drop`) per operasi secara linear.
* **Insiden Tabrakan**: Peningkatan suhu gudang (`ambient_temp_c`) di atas $30^{\circ}\text{C}$ sangat berkorelasi dengan naiknya tingkat tabrakan robot (`collision_count`). Hal ini kemungkinan disebabkan oleh panas berlebih (*overheating*) pada sensor laser/kamera robot yang mendistorsi deteksi objek.

---

## 3. Implikasi bagi Perancangan Model Reinforcement Learning (RL)

> [!IMPORTANT]
> Temuan EDA di atas sangat memengaruhi penentuan elemen-elemen penting dalam perancangan Model RL untuk 5 agen kita:

### 1. Agen Navigasi & Baterai (Routing RL)
* **State Space**: Tambahkan parameter `payload_weight_kg` dan `ambient_temp_c`.
* **Reward**: Berikan penalti berat jika robot dipaksa berjalan pada kecepatan penuh (`max_speed_mps`) di suhu panas ($>30^{\circ}\text{C}$) demi mencegah tabrakan.

### 2. Agen Pemeliharaan Preventif (Maintenance Scheduler RL)
* **State Space**: Masukkan `recurrence_count`, `downtime_hours`, sertifikasi teknisi, dan performa teknisi (`performance_score`).
* **Action Space**: Alokasikan teknisi *Master Tech* khusus untuk menangani robot dengan kasus kerusakan berulang tinggi.
* **Reward**: Maksimalkan nilai utilisasi robot dengan menetapkan fungsi peminimalkan total cost (downtime cost + labor rate).

### 3. Agen Dispatcher Tugas (Task Allocator RL)
* **State Space**: Jam harian (`hour`), kapasitas antrean zona (`current_occupancy_pct`), dan level daya baterai robot.
* **Action Space**: Rutekan tugas ke robot yang berada di dekat zona pengerjaan untuk menghindari kemacetan di staging area.
* **Reward**: Berikan penalti jika menugaskan robot dengan sisa baterai $<20\%$ untuk tugas berjarak jauh (`distance_m`).
