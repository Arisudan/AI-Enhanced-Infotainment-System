import cv2
from deepface import DeepFace

# Start webcam
cap = cv2.VideoCapture(0)

print("[INFO] Starting webcam... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    try:
        # Analyze emotions (faster model: 'Emotion' backend is 'Fer')
        result = DeepFace.analyze(frame,
                                  actions=['emotion'],
                                  enforce_detection=False,
                                  detector_backend='opencv')  # Use fast detector
        emotion = result[0]['dominant_emotion']

        # Display result
        cv2.putText(frame, f'Emotion: {emotion}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print("Error:", e)

    cv2.imshow('Emotion Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
