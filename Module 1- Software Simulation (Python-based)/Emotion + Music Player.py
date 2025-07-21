import cv2
import os
import time
import random
from deepface import DeepFace
import pygame

# Define music folders based on emotion
music_folders = {
    'happy': r'D:\Project Z\Emotion Songs\Happy',
    'sad': r'D:\Project Z\Emotion Songs\Sad',
    'few': r'D:\Project Z\Emotion Songs\Few'  # for neutral, fear, angry, surprise
}

# Initialize webcam
cap = cv2.VideoCapture(0)
emotion_samples = []

print("[INFO] Capturing 10 frames to determine your emotion...")
valid_frames = 0

while valid_frames < 10:
    ret, frame = cap.read()
    if not ret:
        continue

    try:
        # Analyze frame
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='retinaface'  # better than opencv
        )
        emotion = result[0]['dominant_emotion']
        confidence = result[0]['emotion'][emotion]

        if confidence > 50:  # only accept strong predictions
            emotion_samples.append(emotion)
            valid_frames += 1
            print(f"[{valid_frames}/10] {emotion} ({confidence:.1f}%)")

            # Display on screen
            cv2.putText(frame, f'{emotion} ({int(confidence)}%)', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        else:
            print(f"[Low Confidence] Skipping frame")

    except Exception as e:
        print("[ERROR]", e)

    # Resize to full screen
    screen_res = 1280, 720
    scale_width = screen_res[0] / frame.shape[1]
    scale_height = screen_res[1] / frame.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(frame.shape[1] * scale)
    window_height = int(frame.shape[0] * scale)
    frame_resized = cv2.resize(frame, (window_width, window_height))

    cv2.imshow("Emotion Sampling", frame_resized)
    cv2.waitKey(700)

# Final emotion decision
cap.release()
cv2.destroyAllWindows()

from collections import Counter
most_common_emotion = Counter(emotion_samples).most_common(1)[0][0]
print(f"\n🎯 Dominant Emotion: {most_common_emotion.upper()}")

# Choose folder based on emotion
if most_common_emotion in ['happy']:
    folder = music_folders['happy']
elif most_common_emotion in ['sad']:
    folder = music_folders['sad']
else:
    folder = music_folders['few']

# Play music from folder
print(f"\n🎵 Now playing songs from: {folder}")
pygame.init()
pygame.mixer.init()

song_files = [file for file in os.listdir(folder) if file.endswith(('.mp3', '.wav'))]
if not song_files:
    print("No audio files found in the folder.")
    exit()

for song in song_files:
    song_path = os.path.join(folder, song)
    print(f"Playing: {song}")
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    # Wait until song finishes
    while pygame.mixer.music.get_busy():
        time.sleep(1)

print("✅ All songs played. Exiting.")
pygame.quit()
