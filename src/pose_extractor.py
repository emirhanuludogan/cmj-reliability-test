import cv2
import mediapipe as mp
import numpy as np

def extract_pose_data(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=0,  # Lite model (hızlı ve hafif)
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if fps == 0 or np.isnan(fps):
        fps = 60.0 

    t_data = []
    com_y_data = []
    ankle_y_data = []
    
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        h, w, _ = frame.shape
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # GÖRÜNÜRLÜK AĞIRLIKLI KÜTLE MERKEZİ (Visibility-Weighted CoM)
            l_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h
            l_hip_vis = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility
            
            r_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * h
            r_hip_vis = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility
            
            # Kapanan uzvun (occlusion) çöp verisini dışlayan matematik
            com_y = (l_hip_y * l_hip_vis + r_hip_y * r_hip_vis) / (l_hip_vis + r_hip_vis + 1e-6)
            
            # GÖRÜNÜRLÜK AĞIRLIKLI AYAK BİLEĞİ (Uçuş Tespiti İçin)
            l_ankle_y = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h
            l_ankle_vis = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].visibility
            
            r_ankle_y = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * h
            r_ankle_vis = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].visibility
            
            ankle_y = (l_ankle_y * l_ankle_vis + r_ankle_y * r_ankle_vis) / (l_ankle_vis + r_ankle_vis + 1e-6)
            
            t = frame_count / fps
            
            t_data.append(t)
            com_y_data.append(com_y)
            ankle_y_data.append(ankle_y)
            
        frame_count += 1

    cap.release()
    pose.close()
    
    return np.array(t_data), np.array(com_y_data), np.array(ankle_y_data)