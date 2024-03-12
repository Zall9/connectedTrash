import cv2
#cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("test not working")
    exit()
else:
    print("opened")
# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

ret, frame = cap.read()

if not ret:
    print("cant receive frame")
    exit()

cv2.imwrite('image.jpg', frame)
cap.release()

