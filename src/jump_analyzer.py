import numpy as np

def analyze_jump(t_data, com_y_data, ankle_y_data):
    """
    Zaman ve piksel konum verilerinden CMJ sıçrama yüksekliğini hesaplar.
    Maildeki talimatlara uygun olarak uçuş evresi polinomu (polyfit) ile kalibre edilmiştir.
    """
    # 1. En Yüksek Noktayı (Peak) Bul
    peak_idx = np.argmin(com_y_data)
    
    # 2. Uçuş Evresini Kesin Olarak Belirle
    initial_ankle_y = np.mean(ankle_y_data[:30])
    threshold_y = initial_ankle_y - (np.max(ankle_y_data) - np.min(ankle_y_data)) * 0.15
    
    start_idx = peak_idx
    while start_idx > 0 and ankle_y_data[start_idx] < threshold_y:
        start_idx -= 1
        
    end_idx = peak_idx
    while end_idx < len(ankle_y_data) - 1 and ankle_y_data[end_idx] < threshold_y:
        end_idx += 1
    
    # 3. Saf Serbest Düşme (Pure Flight) Evresi ve Dinamik Ölçek (Parabol)
    # Baştan ve sondan 2'şer kare (toplam ~0.06 saniye) kırparak yeri itme/darbe emme kas kuvvetlerini çıkarıyoruz
    trim = 2
    pure_start = start_idx + trim
    pure_end = end_idx - trim
    
    if pure_end - pure_start < 3:
        pure_start = start_idx
        pure_end = end_idx
        
    t_flight = t_data[pure_start:pure_end]
    com_y_flight = com_y_data[pure_start:pure_end]
    
    if len(t_flight) < 3:
         return {"error": "Polinom hesaplaması için yeterli uçuş verisi yok."}
         
    # Mail kuralı: y = at^2 + bt + c -> a'yı çek, pixel_per_meter = 2a / 9.81
    coeffs = np.polyfit(t_flight, com_y_flight, 2)
    a = coeffs[0]
    
    if a <= 0:
        return {"error": "Parabolik serbest düşüş (a > 0) hesaplanamadı."}
        
    pixel_per_meter = (2 * a) / 9.81
    
    # 4. Gerçek Sabit Duruş (Baseline) Çizgisini Bul (Zaman Bağımsız Yeni Matematik)
    # Kişinin videoda ne kadar beklediğinden bağımsız olarak, 
    # çömelmeden önceki "tam dik durduğu" an, kütle merkezinin en yukarıda (Y pikselinin en küçük) olduğu andır.
    
    search_start = 30  # İlk 0.5 saniyeyi (kamera titremesi ihtimaline karşı) atla
    search_end = start_idx # Sıçrama anına (havalanmaya) kadar tara
    
    if search_end - search_start >= 15:
        # 15 karelik (0.25 saniye) pencerelerle kütle merkezinin hareketini pürüzsüzleştiriyoruz
        # Bu pencereler arasındaki en küçük Y değeri (fiziksel en yüksek konum), kişinin dik durduğu sabit andır.
        rolling_windows = [np.mean(com_y_data[i:i+15]) for i in range(search_start, search_end - 15)]
        best_baseline_y = min(rolling_windows)
    else:
        # Eğer video çok kısaysa (bekleme hiç yoksa) sıçramadan önceki mevcut kısmı al
        best_baseline_y = np.mean(com_y_data[:max(1, start_idx)])
    # 5. Yükseklik Hesaplama
    peak_y = com_y_data[peak_idx]
    
    jump_height_pixels = best_baseline_y - peak_y
    jump_height_meters = jump_height_pixels / pixel_per_meter
    
    return {
        "baseline_com_y": round(best_baseline_y, 2),
        "peak_y": round(peak_y, 2),
        "a_coefficient": round(a, 4),
        "pixel_per_meter": round(pixel_per_meter, 2),
        "jump_height_cm": round(jump_height_meters * 100, 2),
        "jump_height_m": round(jump_height_meters, 4)
    }