import cv2
import mediapipe as mp
import os
from main import test_sessions  # Tüm test videolarını main.py'den otomatik çekiyoruz

# Yollar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DIR = os.path.join(BASE_DIR, "data", "raw_videos")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def create_presentation_video(video_filename, output_filename):
    video_path = os.path.join(VIDEO_DIR, video_filename)
    output_path = os.path.join(RESULTS_DIR, output_filename)
    
    if not os.path.exists(video_path):
        print(f"HATA: {video_filename} bulunamadı.")
        return

    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Sunum için video kaydedici
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps if fps > 0 else 60.0, (width, height))

    print(f"\n[İŞLENİYOR] {video_filename} -> Canlı izleme ekranına aktarılıyor...")

    # Ekran boyutlandırma ayarı (Taşmaları önlemek için)
    window_name = 'MediaPipe CMJ Sunum Gorsellestirici'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 540, 960) # Dizüstü bilgisayar ekranına sığacak ideal dik format

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
            landmarks = results.pose_landmarks.landmark
            l_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            r_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            
            l_hip_x, l_hip_y = l_hip.x * width, l_hip.y * height
            r_hip_x, r_hip_y = r_hip.x * width, r_hip.y * height
            
            # Görünürlük ağırlıklı kütle merkezi formülü
            com_x = int((l_hip_x * l_hip.visibility + r_hip_x * r_hip.visibility) / (l_hip.visibility + r_hip.visibility + 1e-6))
            com_y = int((l_hip_y * l_hip.visibility + r_hip_y * r_hip.visibility) / (l_hip.visibility + r_hip.visibility + 1e-6))
            
            cv2.circle(frame, (com_x, com_y), 15, (0, 0, 255), -1)
            cv2.putText(frame, "Kutle Merkezi (CoM)", (com_x + 20, com_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Kapanma/Occlusion Uyarısı
            if l_hip.visibility < 0.7 or r_hip.visibility < 0.7:
                cv2.putText(frame, "UYARI: GORSEL KAPANMA (OCCLUSION)!", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.putText(frame, "Model kalcayi gormekte zorlaniyor!", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            else:
                cv2.putText(frame, "TAKIP BASARILI", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        out.write(frame)

        cv2.imshow(window_name, frame)
        
        # 'q' tuşuna basarsan o videoyu atlar, diğerine geçer
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Video atlandı.")
            break

    cap.release()
    out.release()
    pose.close()

if __name__ == "__main__":
    print("Toplu video işleme ve canlı izleme başlatılıyor...")
    
    # main.py içindeki test_sessions sözlüğünü dönerek tüm videoları sırayla işler
    for session_id, data in test_sessions.items():
        # Önce Ön Açıyı işler ve ekrana yansıtır
        create_presentation_video(data["front"], f"SUNUM_{session_id}_on.mp4")
        # Sonra aynı denemenin Yan Açısını işler ve ekrana yansıtır
        create_presentation_video(data["side"], f"SUNUM_{session_id}_yan.mp4")
        
    cv2.destroyAllWindows()
    print("\nTüm videolar başarıyla görselleştirildi ve kaydedildi!")