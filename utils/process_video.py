import cv2
import numpy as np
import mediapipe as mp
import pandas as pd
from collections import Counter
from tensorflow.keras.models import load_model
import pickle
import os

# Load scaler
with open("models/scaler.pkl", "rb") as f:
    new_df_scaler = pickle.load(f)

# Load trained models
model_paths = {
    'CNN_GRU': 'models/CNN_GRU.h5',
    'RNN': 'models/RNN.h5',
    'CNN_LSTM': 'models/CNN_LSTM.h5',
    'Autoencoder_Classifier': 'models/Autoencoder_Classifier.h5'
}

models = {name: load_model(path) for name, path in model_paths.items()}

# Class labels
class_labels = {
    0: "Normal",
    1: "Limping",
    2: "Slouch",
    3: "No Arm Swing",
    4: "Concriduction"
}

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def extract_keypoints(video_path, max_frames=200, output_path=None):
    cap = cv2.VideoCapture(video_path)
    keypoints_data = []
    
    frame_count = 0
    # Use the 'mp4v' codec (as it worked previously for you)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Write to the provided output_path if set
    if output_path:
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        if not out.isOpened():
            print("Error: VideoWriter failed to open with path:", output_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_count >= max_frames:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            row = []
            for landmark in results.pose_landmarks.landmark:
                row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            keypoints_data.append(row)

            # Draw landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if output_path:
            out.write(frame)

        frame_count += 1

    cap.release()
    if output_path:
        out.release()

    if keypoints_data:
        df = pd.DataFrame(keypoints_data)
        df = df.fillna(0)
        df_scaled = new_df_scaler.transform(df)
        df_reshaped = df_scaled.reshape(df_scaled.shape[0], 33, 4)
        return df_reshaped

    return None

def process_video(video_path, output_folder):
    # Create a processed filename based on the original filename
    processed_video_name = f"processed_{os.path.basename(video_path)}"
    processed_video_path = os.path.join(output_folder, processed_video_name)

    keypoints = extract_keypoints(video_path, output_path=processed_video_path)

    if keypoints is None:
        return {"error": "No keypoints detected"}

    final_predictions = []
    model_results = {}

    for model_name, model in models.items():
        predictions = model.predict(keypoints)
        predicted_classes = np.argmax(predictions, axis=1).astype(int)
        counter = Counter(predicted_classes)

        most_common_class = counter.most_common(1)
        overall_prediction = class_labels.get(most_common_class[0][0], "Unknown") if most_common_class else "No valid predictions"

        final_predictions.extend(predicted_classes)
        model_results[model_name] = {
            "distribution": {class_labels.get(k, "Unknown"): v for k, v in counter.items()},
            "overall_prediction": overall_prediction
        }

    final_counter = Counter(final_predictions)
    final_prediction = class_labels.get(final_counter.most_common(1)[0][0], "Unknown")

    # Build a new filename for the converted video
    converted_video_path = processed_video_path.replace('.mp4', '_converted.mp4')

    # Quote paths in the FFmpeg command to handle spaces or special characters
    ffmpeg_command = f'ffmpeg -i "{processed_video_path}" -c:v libx264 -pix_fmt yuv420p -crf 23 -preset fast -c:a aac -b:a 128k "{converted_video_path}"'
    os.system(ffmpeg_command)

    return {
        "models": model_results,
        "final_prediction": final_prediction,
        "processed_video": os.path.basename(converted_video_path)
    }
