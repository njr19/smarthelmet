# smart_helmet_demo.py
import cv2
import os
import time
from collections import deque

# --- Settings ---
BUFFER_SIZE = 10           # frames for stable detection
SLOWDOWN_STEP = 20
SLOWDOWN_INTERVAL = 1.0
# ----------------

# Load cascades
helmet_path = os.path.join(os.getcwd(), "helmet.xml")
helmet_cascade = cv2.CascadeClassifier(helmet_path)
if helmet_cascade.empty():
    print("Error: Could not load helmet.xml")
    exit()

face_cascade_front = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
face_cascade_profile = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

# Video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

bike_running = False
speed = 0
last_slow_time = time.time()
det_buffer = deque(maxlen=BUFFER_SIZE)

print("Press 'q' to quit. Put helmet on for demo.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = list(face_cascade_front.detectMultiScale(gray, 1.1, 5, minSize=(80,80)))
    faces += list(face_cascade_profile.detectMultiScale(gray, 1.1, 5, minSize=(80,80)))

    # Detect helmets
    helmets = helmet_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50,50))
    helmet_detected_frame = False

    # Check helmets above detected faces
    for (hx,hy,hw,hh) in helmets:
        for (fx,fy,fw,fh) in faces:
            if hy+hh < fy + fh//2:  # helmet is above head
                helmet_detected_frame = True
                cv2.rectangle(frame, (hx,hy), (hx+hw, hy+hh), (0,255,0),2)

    # Update detection buffer
    det_buffer.append(1 if helmet_detected_frame else 0)
    helmet_now = sum(det_buffer) > len(det_buffer)//2

    # Bike state logic
    now = time.time()
    if not bike_running:
        if helmet_now:
            bike_running = True
            speed = 100
            print("[SYSTEM] Helmet ON ✅ → Bike started 🏍️")
        else:
            speed = 0
    else:
        if not helmet_now:
            if now - last_slow_time >= SLOWDOWN_INTERVAL:
                last_slow_time = now
                speed = max(0, speed - SLOWDOWN_STEP)
                print(f"[SYSTEM] Helmet removed ❌ → Slowing... Speed={speed}%")
            if speed == 0:
                bike_running = False
                print("[SYSTEM] Bike stopped due to helmet removal 🛑")
        else:
            speed = min(100, speed + 10)

    # Overlay text
    status_text = "RUNNING" if bike_running else "STOPPED"
    helmet_text = "Helmet: YES" if helmet_now else "Helmet: NO"
    cv2.putText(frame, f"Status: {status_text}", (10,30), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    cv2.putText(frame, helmet_text, (10,60), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0) if helmet_now else (0,0,255),2)
    cv2.putText(frame, f"Speed: {speed}%", (10,90), cv2.FONT_HERSHEY_SIMPLEX,0.7,(200,200,0),2)

    # Speed bar
    bar_x, bar_y = frame.shape[1]-150, frame.shape[0]-40
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x+100, bar_y+20), (50,50,50), -1)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x+int(speed), bar_y+20), (0,200,0) if bike_running else (0,100,200), -1)
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x+100, bar_y+20), (255,255,255), 1)

    cv2.imshow("Smart Helmet Demo", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
