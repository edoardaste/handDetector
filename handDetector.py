import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
Hands = mp_hands.Hands(max_num_hands=1)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()

    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)

    h, w, _ = image.shape
    fingerPoints = []
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS)
        for id, cord in enumerate(hand_landmarks.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                cv2.putText(image, str(id), (cx, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                fingerPoints.append((cx,cy))
                
        dedos = [8,12,16,20]
        contador = 0
        if fingerPoints:
            if fingerPoints[4][0] < fingerPoints[3][0]:
               contador += 1
            for x in dedos:
              if fingerPoints[x][1] < fingerPoints[x-2][1]:
                 contador +=1
                       
        cv2.rectangle(image, (80, 10), (200,110), (255, 0, 0), -1)
        cv2.putText(image,str(contador),(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(255,255,255),5)

        
        
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()