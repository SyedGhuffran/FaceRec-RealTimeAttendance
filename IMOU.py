import cv2

camera_url = "rtsp://admin:L2681A0E@192.168.2.230:37777/live"
cap = cv2.VideoCapture(camera_url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("kuch masla hai")
        break

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
