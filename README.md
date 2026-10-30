# MediaPipe CMJ (Countermovement Jump) Analiz ve Kalibrasyon Sistemi

Bu proje, spor biyomekaniğinde yaygın olarak kullanılan Countermovement Jump (CMJ) sıçrama testlerini 2D kamera görüntüleri üzerinden analiz eden, MediaPipe Pose Lite tabanlı otonom bir ölçüm sistemidir. 

## 🚀 Proje Amacı ve Çözülen Problemler
Geleneksel görüntü işleme tabanlı sıçrama ölçümlerinde (Kinovea vb.) referans noktalarının manuel seçilmesi ve farklı kamera açılarının yarattığı sapmalar en büyük problemlerdir. Bu proje:
* Sıçrama yüksekliğini pikselden santimetreye çevirmek için **uçuş evresi parabolik polinomu (polyfit)** kullanarak dinamik ve otomatik bir `pixel-to-meter` kalibrasyonu yapar.
* Sıçrama öncesi dik duruş pozisyonunu (baseline) saniye kısıtlamalarından bağımsız, **sinyal pürüzsüzleştirme (smoothing)** ile minimum Y koordinatını bularak otonom şekilde tespit eder.
* **Görünürlük Ağırlıklı (Visibility-Weighted)** kütle merkezi (CoM) formülü kullanarak kapanan/örtüşen (occlusion) uzuvların yarattığı takip hatalarını minimuma indirir.

## 📊 Bulgular: Ön Kamera vs. Yan Kamera
Yapılan A/B testleri ve Kinovea referans karşılaştırmaları sonucunda:
1. **Ön Açı (Front View):** Ortalama **~1.25 cm** hata payı ile Kinovea referanslarına (Altın Standart) mükemmel uyum sağlamıştır. Her iki kalça da net göründüğü için kütle merkezi takibi kusursuzdur.
2. **Yan Açı (Side View):** Yan çekimlerde (eller belde pozisyonunda) kolların kalça eklemini kapatması (Occlusion) nedeniyle MediaPipe'ın tahmin zorluğu yaşadığı ve hatanın **~3.27 cm** seviyelerine çıktığı tespit edilmiştir. Omuz destekli (Torso) alternatif merkez denemelerinde ise gövde bükülmesi (trunk flexion) nedeniyle hatanın daha da arttığı kanıtlanmıştır.
**Sonuç:** CMJ ölçümlerinde optik ve biyomekanik doğruluğun sağlanması için ürün standartlarında **sadece ön kamera (front view)** kullanılmalıdır.

## 🛠️ Kurulum
Projeyi lokalinizde çalıştırmak için:

1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/emirhanuludogan/cmj-reliability-test.git](https://github.com/emirhanuludogan/cmj-reliability-test.git)
   cd cmj-reliability-test