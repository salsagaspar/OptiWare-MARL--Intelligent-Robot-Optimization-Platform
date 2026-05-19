# ROI & Business Simulation Results: AI/RL-Based Predictive Maintenance

---

## 1. Visualisasi Analisis Keuangan Proyek
Berikut adalah grafik visualisasi hasil simulasi keuangan proyek armada **300 robot gudang** selama periode proyeksi 3 tahun. Gunakan Carousel untuk menelusuri grafik.

````carousel
![Perbandingan Pengeluaran Armada Tahunan](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\fleet_cost_comparison.png)
<!-- slide -->
![Kurva Balik Modal Kumulatif (Payback Curve)](C:\Users\hpvic\.gemini\antigravity\brain\57dff280-9f46-4106-a18d-4d1bf353dcfe\artifacts\cumulative_cash_flow_curve.png)
````

---

## 2. Metrik Kunci Kelayakan Investasi (Armada 300 Robot)

| Metrik Keuangan | Nilai Pemodelan | Kategori Evaluasi | Penafsiran Bisnis |
| :--- | :---: | :---: | :--- |
| **Investasi Awal (CapEx)** | **\$500,000.00** | Netral | Biaya lisensi AI, upgrade sensor hardware, & integrasi sistem. |
| **Aliran Kas Masuk Bersih / Tahun** | **\$1,341,526.00** | Sangat Tinggi | Penghematan tahunan (\$1.39M) dikurangi biaya operasional OpEx (\$50K). |
| **Net Present Value (NPV @10%)** | **\$2,836,176.60** | **Sangat Layak ($>0$)** | Menunjukkan nilai tambah bersih yang besar bagi kekayaan perusahaan. |
| **Internal Rate of Return (IRR)** | **262.7%** | **Sangat Superior** | Jauh melampaui biaya modal rata-rata (*Weighted Average Cost of Capital*). |
| **Waktu Balik Modal (Payback Period)** | **4.5 Bulan** | **Sangat Cepat** | Seluruh modal awal kembali hanya dalam waktu kurang dari setengah tahun. |
| **Return on Investment (ROI 3-Tahun)**| **704.9%** | **Sangat Tinggi** | Setiap \$1 yang diinvestasikan menghasilkan \$7.05 keuntungan bersih setelah 3 tahun. |

---

## 3. Analisis & Pembahasan Kelayakan Bisnis

> [!NOTE]
> Proyeksi keuangan ini membuktikan bahwa biaya pencegahan (preventif) jauh lebih murah dibandingkan membiarkan kegagalan operasional terjadi secara tidak terduga di dalam gudang:

1. **Pemangkasan Biaya Tidak Langsung (Indirect Cost Disruption)**:
   * Kebijakan reaktif (Run-to-Failure) memakan biaya disrupsi throughput gudang sebesar **\$1,500,000.00 per tahun** (akibat 2 kali breakdown per robot secara darurat pada armada 300 robot).
   * Kebijakan RL-Based PM berhasil menekan insiden breakdown darurat hingga **0 kali**, sepenuhnya mengeliminasi kerugian tidak langsung ini.
2. **Efisiensi Biaya Langsung (Downtime & Labor)**:
   * Meskipun biaya servis langsung kebijakan RL sedikit lebih tinggi (\$1.86M vs \$1.75M) karena melakukan perawatan berkala secara teratur, biaya ini terserap sepenuhnya oleh hilangnya biaya kegagalan darurat yang mahal (\$1000 per kejadian) serta penalti downtime operasional (\$100/jam).
3. **Analisis Sensitivitas & Risiko**:
   * Bahkan jika tingkat kegagalan sensor naik atau efisiensi agen RL berkurang sebesar 30%, payback period proyek ini masih berada di bawah **7 bulan**, menjadikannya investasi berisiko sangat rendah (*low risk, high return*).

---

## 4. Rekomendasi Strategis untuk Eksekutif Bisnis

> [!TIP]
> Berdasarkan kelayakan finansial yang sangat kuat, disarankan untuk mengambil langkah taktis berikut:
> 1. **Persetujuan Anggaran (Budget Approval)**: Segera cairkan dana CapEx \$500,000 untuk pengembangan sistem pemeliharaan prediktif berbasis RL.
> 2. **Fase Peluncuran Bertahap (Phased Rollout)**: Terapkan model RL pertama kali pada 30 robot di zona tersibuk (`Zone-A` dan `Zone-B`) untuk memvalidasi algoritma secara langsung selama 30 hari sebelum meluncurkan ke seluruh 300 robot.
> 3. **Penyelarasan Kontrak Vendor**: Optimalkan penjadwalan shift teknisi Master Tech untuk menyesuaikan dengan jendela keputusan optimal agen RL (setiap ~1.000 jam operasional).
