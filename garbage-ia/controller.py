import yolov5
import RPi.GPIO as IO

from motor import GroveServo
from numpy import interp

# load model
model = yolov5.load('keremberke/yolov5s-garbage')

# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

# set image
img = "https://i.ytimg.com/vi/ZN3tXr2_CJ0/maxresdefault.jpg"

# perform inference
results = model(img, size=640)

# inference with test time augmentation
results = model(img, augment=True)

# parse results
predictions = results.pred[0]
boxes = predictions[:, :4] # x1, y1, x2, y2
scores = predictions[:, 4]
categories = predictions[:, 5]

classes = ['plastic', 'metal', 'paper', 'glass', 'cardboard']

results.pandas().xyxy[0].sort_values(by='confidence', ascending=False, inplace=True)
best_result = results.pandas().xyxy[0].iloc[0]

print(f'Best result: {best_result["name"]} with confidence {best_result["confidence"]}')

is_plastic = best_result["name"] == "plastic"

print("start")
motor = GroveServo(12)
motor.reset()
if(is_plastic):
    print("right")
    motor.right()
else:
    print("left")
    motor.left()
motor.pwm.stop()
