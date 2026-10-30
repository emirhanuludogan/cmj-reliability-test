# MediaPipe CMJ (Countermovement Jump) Analiz ve Kalibrasyon Sistemi

> Python tabanlı, MediaPipe Pose Lite ve parabolik uçuş fazı kalibrasyonu kullanan otonom biyomekanik sıçrama analiz sistemi.

---

### 🎥 Sistem Görselleştirme Önizlemesi (Occlusion & CoM Tracking)
*Aşağıda sistemin kütle merkezi (CoM) takibi ve görsel kapanma (occlusion) algılama anı yer almaktadır:*

<p align="center">
  <img src="results/cmj_demo.gif" alt="CMJ Analysis Demo" width="300"/>
</p>

---

## 📏 Fiziksel Kalibrasyon ve Referans Çubuğu Standardı
Saha testlerinde ve Kinovea manuel ölçümlerinde mutlak doğruluk sağlamak amacıyla duvara değil, sporcunun hemen yanına dikey bir referans çubuğu yerleştirilmiştir:
* **Toplam Boy:** En üstteki beyaz çizgiden en alttaki beyaz çizgiye kadar tam **100 cm (1 metre)** olarak kalibre edilmiştir.
* **Ara Ölçü:** En üstteki beyaz çizgiden ortadaki beyaz çizgiye kadar olan mesafe ise **40 cm**'dir.
* Kinovea altın standart ölçümleri ve modelin doğrulama kıyaslamaları bu fiziksel referans ölçeğine dayanmaktadır.

---

## 📊 Test Sonuçları (Özet Tablo)
Sistemimizin ürettiği `metrics_output.csv` verilerine göre ön ve yan açıların Kinovea altın standart referanslarıyla karşılaştırma özeti:

| Deneme ID | Kinovea Ön Ref (cm) | Kinovea Yan Ref (cm) | Model Ön Yükseklik (cm) | Model Yan Yükseklik (cm) | Ön Açı Hatası (cm) | Yan Açı Hatası (cm) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **ejmo_deneme1** | 30.99 | 28.13 | 31.18 | 31.37 | 0.19 | 3.24 |
| **ejmo_deneme2** | 34.96 | 26.78 | 32.61 | 27.44 | 2.35 | 0.66 |
| **ejmo_deneme3** | 34.45 | 26.83 | 34.08 | 32.58 | 0.37 | 5.75 |
| **ulu_deneme1** | 37.23 | 33.35 | 39.28 | 31.59 | 2.05 | 1.76 |
| **ulu_deneme2** | 39.73 | 32.35 | 37.93 | 35.38 | 1.80 | 3.03 |
| **ulu_deneme3** | 41.72 | 36.38 | 40.93 | 41.47 | 0.79 | 5.09 |

---

## 🚀 Proje Amacı ve Çözülen Problemler
Geleneksel görüntü işleme tabanlı sıçrama ölçümlerinde (Kinovea vb.) referans noktalarının manuel seçilmesi ve farklı kamera açılarının yarattığı sapmalar en büyük problemlerdir. Bu proje:
* Sıçrama yüksekliğini pikselden santimetreye çevirmek için **uçuş evresi parabolik polinomu (polyfit)** kullanarak dinamik ve otomatik bir `pixel-to-meter` kalibrasyonu yapar.
* Sıçrama öncesi dik duruş pozisyonunu (baseline) saniye kısıtlamalarından bağımsız, sinyal pürüzsüzleştirme ile minimum Y koordinatını bularak otonom şekilde tespit eder.
* **Görünürlük Ağırlıklı (Visibility-Weighted)** kütle merkezi (CoM) formülü kullanarak kapanan/örtüşen (occlusion) uzuvların yarattığı takip hatalarını minimuma indirir.

---

## 📊 Bulgular: Ön Kamera vs. Yan Kamera (A/B Testi)
Yapılan testler sonucunda:
1. **Ön Açı (Front View):** Ortalama **~1.25 cm** hata payı ile Kinovea referanslarına mükemmel uyum sağlamıştır.
2. **Yan Açı (Side View):** Eller belde pozisyonunda kolların kalçayı kapatması (occlusion) nedeniyle modelin zorlandığı ve hatanın arttığı gözlemlenmiştir. 
**Sonuç:** CMJ ölçümlerinde optik ve biyomekanik güvenilirlik için ön kamera (front view) kullanımı önerilir.

---

## 🛠️ Kurulum ve Kullanım
Projeyi lokalinizde çalıştırmak için:

1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/emirhanuludogan/cmj-reliability-test.git](https://github.com/emirhanuludogan/cmj-reliability-test.git)
   cd cmj-reliability-test