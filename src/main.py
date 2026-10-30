import os
import pandas as pd
from pose_extractor import extract_pose_data
from jump_analyzer import analyze_jump

# Yolların Belirlenmesi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE_DIR, "data", "raw_videos")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Sonuç klasörü yoksa oluştur
os.makedirs(RESULTS_DIR, exist_ok=True)

# Yarınki test verileri için örnek yapı (Gerçek isimler ve ölçümlerle güncellenecek)
# Format -> "Deneme_ID": {"front": "on_video.mp4", "side": "yan_video.mp4", "kinovea_ref_m": 0.45}
test_sessions = {
    # EJMO Denemeleri
    "ejmo_deneme1": {
        "front": "deneme1_on_ejmo.mov",
        "side": "deneme1_yan_ejmo.mov",
        "kinovea_ref_front_m": 0.3099,
        "kinovea_ref_side_m": 0.2813
    },
    "ejmo_deneme2": {
        "front": "deneme2_on_ejmo.mov",
        "side": "deneme2_yan_ejmo.mov",
        "kinovea_ref_front_m": 0.3496,
        "kinovea_ref_side_m": 0.2678
    },
    "ejmo_deneme3": {
        "front": "deneme3_on_ejmo.mov",
        "side": "deneme3_yan_ejmo.mov",
        "kinovea_ref_front_m": 0.3445,
        "kinovea_ref_side_m": 0.2683
    },
    
    # ULU Denemeleri
    "ulu_deneme1": {
        "front": "deneme1_on_ulu.mov",
        "side": "deneme1_yan_ulu.mov",
        "kinovea_ref_front_m": 0.3723,
        "kinovea_ref_side_m": 0.3335
    },
    "ulu_deneme2": {
        "front": "deneme2_on_ulu.mov",
        "side": "deneme2_yan_ulu.mov",
        "kinovea_ref_front_m": 0.3973,
        "kinovea_ref_side_m": 0.3235
    },
    "ulu_deneme3": {
        "front": "deneme3_on_ulu.mov",
        "side": "deneme3_yan_ulu.mov",
        "kinovea_ref_front_m": 0.4172,
        "kinovea_ref_side_m": 0.3638
    }
}

def process_video(video_filename):
    video_path = os.path.join(VIDEO_DIR, video_filename)
    if not os.path.exists(video_path):
        return None
        
    t_data, com_y_data, ankle_y_data = extract_pose_data(video_path)
    result = analyze_jump(t_data, com_y_data, ankle_y_data)
    return result


def main():
    results_list = []
    
    for session_id, data in test_sessions.items():
        print(f"[{session_id}] İşleniyor...")
        
        # Ön açı işlemleri
        front_res = process_video(data["front"])
        # Yan açı işlemleri
        side_res = process_video(data["side"])
        
        if front_res is None or side_res is None or "error" in front_res or "error" in side_res:
            print(f"HATA: {session_id} işlenemedi veya dosyalar eksik.")
            continue
            
        # Analizden gelen hazır SANTİMETRE değerlerini çekiyoruz
        front_h_cm = front_res["jump_height_cm"]
        side_h_cm = side_res["jump_height_cm"]
        
        # Sözlüğe girdiğin metre değerlerini 100 ile çarpıp cm'ye çeviriyoruz
        front_ref_cm = data["kinovea_ref_front_m"] * 100
        side_ref_cm = data["kinovea_ref_side_m"] * 100
        
        # Karşılaştırma ve Hata Hesaplamaları (Artık hepsi cm)
        angle_diff_cm = abs(front_h_cm - side_h_cm) 
        front_error_cm = abs(front_h_cm - front_ref_cm) 
        side_error_cm = abs(side_h_cm - side_ref_cm)    
        
        results_list.append({
            "Deneme ID": session_id,
            "Kinovea Ön Ref (cm)": round(front_ref_cm, 2),
            "Kinovea Yan Ref (cm)": round(side_ref_cm, 2),
            "Model Ön Yükseklik (cm)": round(front_h_cm, 2),
            "Model Yan Yükseklik (cm)": round(side_h_cm, 2),
            "Açılar Arası Fark (cm)": round(angle_diff_cm, 2),
            "Ön Açı Hatası (cm)": round(front_error_cm, 2),
            "Yan Açı Hatası (cm)": round(side_error_cm, 2)
        })
        
    if results_list:
        df = pd.DataFrame(results_list)
        output_path = os.path.join(RESULTS_DIR, "metrics_output.csv")
        df.to_csv(output_path, index=False)
        print(f"\nİşlem Tamamlandı! Sonuçlar kaydedildi: {output_path}")
        print("\n--- ÖZET TABLO ---")
        print(df.to_string())
    else:
        print("İşlenecek geçerli veri bulunamadı.")

if __name__ == "__main__":
    main()