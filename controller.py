import yolov5
import RPi.GPIO as IO
from camera import Camera
from Player import Player
from motor import GroveServo
from numpy import interp

def objectIsPlastic(model, cam):
    cam.screenshot()

    # perform inference
    results = model(img, size=640)

    # inference with test time augmentation
    results = model(img, augment=True)

    # parse results
    predictions = results.pred[0]
    boxes = predictions[:, :4] # x1, y1, x2, y2
    scores = predictions[:, 4]
    categories = predictions[:, 5]

    results.pandas().xyxy[0].sort_values(by='confidence', ascending=False, inplace=True)
    best_result = results.pandas().xyxy[0].iloc[0]

    print(f'Best result: {best_result["name"]} with confidence {best_result["confidence"]}')

    return best_result["name"] == "plastic"
    
def moveTrash(model, cam, choosePlastic):
    is_plastic = objectIsPlastic(model, cam)
    if(is_plastic == choosePlastic):
        player.play()
        if(choosePlastic):
            motor.right()
        else:
            motor.left()
        motor.pwm.stop()
    else:
        player.play(False)
    sleep(1)

# load model
model = yolov5.load('keremberke/yolov5s-garbage')

# set model parameters
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image

cam = Camera()
player = Player()
img = "./image.jpg"

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(6, IO.IN, pull_up_down=IO.PUD_DOWN)
IO.setup(17, IO.IN, pull_up_down=IO.PUD_DOWN)

motor = GroveServo(12)

def button_callback(channel):
    if(channel == 6):
        print('plastic')
        moveTrash(model, cam, True)
    else:
        print('not plastic')
        moveTrash(model, cam, False)
    
print("init finished")

IO.add_event_detect(6,IO.RISING,callback=button_callback)
IO.add_event_detect(17,IO.RISING,callback=button_callback)

#while True:
    # Plastic
    #if IO.input(6) == IO.HIGH:
        #print('plastic')
        #moveTrash(model, cam, True)
    # Not Plastic
    #elif IO.input(17) == IO.HIGH:
        #print('not plastic')
        #moveTrash(model, cam, False)


