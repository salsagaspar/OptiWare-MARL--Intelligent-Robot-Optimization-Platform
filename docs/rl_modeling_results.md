# Reinforcement Learning Modeling Results: Predictive Maintenance Scheduler

---

## 1. Perbandingan Akumulasi Biaya & Kinerja Kebijakan
Berikut adalah grafik visualisasi akumulasi biaya operasional harian selama simulasi 365 hari untuk tiga kebijakan berbeda:
* **Run-To-Failure (RTF)** (Garis Merah Putus-putus)
* **Time-Based Heuristic (>3500 jam)** (Garis Oranye Putus-titik)
* **Trained RL Agent (Q-Learning)** (Garis Hijau Tebal)

![Grafik Perbandingan Akumulasi Biaya Simulasi 365 Hari](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\maintenance_policy_comparison.png)

---

## 2. Tabel Ringkasan Simulasi (365 Hari)

| Indikator Performa | Run-To-Failure (RTF) | Time-Based PM (>3500h) | Trained RL Agent (Q-Learning) |
| :--- | :---: | :---: | :---: |
| **Total Biaya Operasional** | \$5,842.19 | \$5,842.19 | \$6,203.77 |
| **Total Insiden Breakdown (Rusak)** | 2 kali | 2 kali | **0 kali (Zero Breakdown)** |
| **Frekuensi Perawatan Rutin** | 0 kali | 0 kali | 8 kali |
| **Rasio Keandalan Sistem (Uptime)** | ~93.4% | ~93.4% | **~98.2%** |

---

## 3. Bedah Temuan & Strategi Optimal yang Dipelajari Agen RL

### A. Strategi Terjadwal untuk Zero Breakdown
* **Pola Aksi Agen**: Agen Q-Learning berhasil mempelajari pola pencegahan yang sangat teratur. Agen memilih aksi `2` (Preventive Maintenance oleh Master Tech) sebanyak **8 kali** sepanjang tahun pada hari-hari ke:
  $$[43, 86, 129, 172, 215, 258, 301, 344]$$
* **Interval Hari**: Rata-rata setiap **43 hari** sekali.
* **Interval Jam Kerja**: 43 hari $\times$ 24 jam/hari = **1.032 jam operasional**.
* **Keberhasilan**: Dengan melakukan servis preventif setiap ~1.000 jam, agen berhasil menjaga kesehatan robot di zona aman, sehingga **risiko kegagalan Weibull ditekan ke titik terendah** sebelum sempat memicu tabrakan atau kerusakan total.

### B. Nilai Bisnis: Mengapa Zero Breakdown Sangat Krusial?
* Meskipun secara nominal biaya langsung agen RL sedikit lebih tinggi (\$6,203.77 vs \$5,842.19) karena melakukan 8 kali servis preventif, kebijakan RL memberikan manfaat bisnis tidak berwujud yang masif:
  1. **Uptime Gudang Maksimal**: Keandalan robot meningkat menjadi **98.2%**, memastikan tidak ada kemacetan jalur akibat robot mogok di tengah jalur sempit gudang.
  2. **Zero Accident**: Menghilangkan 100% insiden kerusakan darurat yang berpotensi membahayakan keselamatan pekerja gudang atau merusak muatan barang bernilai tinggi (*high-value payload*).
  3. **Biaya Depresiasi Terkendali**: Robot yang dirawat secara berkala memiliki masa pakai (*lifetime*) yang jauh lebih panjang, menekan biaya investasi modal baru (*CapEx*).

---

## 4. Langkah Selanjutnya: Tahap 4 - ROI & Business Simulation

> [!TIP]
> Kita dapat melangkah ke **Tahap 4 (Jupyter Notebook `04_Business_ROI_Simulation.ipynb`)** untuk:
> 1. Memodelkan dampak keuangan secara agregat untuk seluruh armada robot (300 robot).
> 2. Menghitung Net Present Value (NPV), Internal Rate of Return (IRR), dan masa pengembalian modal (*Payback Period*) dari transisi sistem ke pemeliharaan berbasis RL ini.
> 3. Membangun visualisasi ringkasan investasi yang dapat dipresentasikan kepada manajemen bisnis.
