import cv2
import os
import time
import random
from deepface import DeepFace
import pygame
from collections import Counter

# ----------- CONFIG -----------
emotion_sample_count = 10
min_confidence_threshold = 50
process_every_nth_frame = 3
resize_width = 640  # for faster DeepFace processing
# ------------------------------

# Emotion to folder mapping
music_folders = {
    'happy': r'D:\Project Z\Emotion Songs\Happy',
    'sad': r'D:\Project Z\Emotion Songs\Sad',
    'few': r'D:\Project Z\Emotion Songs\Few'  # fear, angry, surprise
}

# Webcam setup
cap = cv2.VideoCapture(0)
emotion_samples = []
frame_count = 0

print("[INFO] Capturing 10 frames to determine your emotion...")

while len(emotion_samples) < emotion_sample_count:
    ret, frame = cap.read()
    if not ret:
        continue

    frame_count += 1
    if frame_count % process_every_nth_frame != 0:
        continue

    # Resize for speed
    resized_frame = cv2.resize(frame, (resize_width, int(frame.shape[0] * resize_width / frame.shape[1])))

    try:
        result = DeepFace.analyze(
            resized_frame,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='retinaface'
        )

        emotion = result[0]['dominant_emotion']
        confidence = result[0]['emotion'][emotion]

        if confidence > min_confidence_threshold:
            emotion_samples.append(emotion)
            print(f"[{len(emotion_samples)}/10] {emotion} ({confidence:.1f}%)")

            # Overlay on screen
            cv2.putText(frame, f'{emotion} ({int(confidence)}%)', (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            print(f"[Low Confidence] Skipped frame")

    except Exception as e:
        print("[ERROR]", e)

    # Resize frame for display without stretching or black bars
    screen_res = 1280, 720
    scale_width = screen_res[0] / frame.shape[1]
    scale_height = screen_res[1] / frame.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(frame.shape[1] * scale)
    window_height = int(frame.shape[0] * scale)
    frame_resized = cv2.resize(frame, (window_width, window_height))

    cv2.imshow("Emotion Sampling", frame_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close webcam and GUI
cap.release()
cv2.destroyAllWindows()

# Determine most frequent emotion
final_emotion = Counter(emotion_samples).most_common(1)[0][0]
print(f"\n🎯 Dominant Emotion: {final_emotion.upper()}")

# Select folder
if final_emotion == 'happy':
    folder = music_folders['happy']
elif final_emotion == 'sad':
    folder = music_folders['sad']
else:
    folder = music_folders['few']

# Play songs from folder
print(f"\n🎵 Playing from: {folder}")
pygame.init()
pygame.mixer.init()

song_files = [file for file in os.listdir(folder) if file.endswith(('.mp3', '.wav'))]
if not song_files:
    print("⚠️ No audio files in the folder.")
    exit()

random.shuffle(song_files)  # Optional: shuffle playlist

for song in song_files:
    song_path = os.path.join(folder, song)
    print(f"▶️ Playing: {song}")
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(1)

print("✅ Playlist complete. Exiting.")
pygame.quit()
