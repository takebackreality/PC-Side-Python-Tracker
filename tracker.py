import cv2
import serial
import time

PORT = "COM3"
BAUD = 115200
arduino = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x = frame_w // 2
center_y = frame_h // 2

pan_angle = 90
tilt_angle = 90

def send_command(cmd):
    arduino.write((cmd + "\n").encode("utf-8"))

lower = (40, 70, 70)
upper = (80, 255, 255)

step_size = 2
tolerance = 30

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        target_x = x + w // 2
        target_y = y + h // 2

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.circle(frame, (target_x, target_y), 5, (0,0,255), -1)

        error_x = target_x - center_x
        error_y = target_y - center_y

        if abs(error_x) > tolerance:
            if error_x > 0: pan_angle -= step_size
            else: pan_angle += step_size
            pan_angle = max(0, min(180, pan_angle))
            send_command(f"PAN{pan_angle}")

        if abs(error_y) > tolerance:
            if error_y > 0: tilt_angle += step_size
            else: tilt_angle -= step_size
            tilt_angle = max(30, min(150, tilt_angle))
            send_command(f"TILT{tilt_angle}")

    cv2.circle(frame, (center_x, center_y), 10, (255,0,0), 2)
    cv2.imshow("Turret Tracker", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("f"):
        send_command("FIRE")
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
