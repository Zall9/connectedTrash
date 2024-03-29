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
    
    try:
        results.pandas().xyxy[0].sort_values(by='confidence', ascending=False, inplace=True)
        best_result = results.pandas().xyxy[0].iloc[0]
    except:
        print("error AI")
        return False
        
    print(f'Best result: {best_result["name"]} with confidence {best_result["confidence"]}')

    return best_result["name"] == "plastic" or best_result["name"] == "paper"
    
def moveTrash(model, cam, choosePlastic):
    is_plastic = objectIsPlastic(model, cam)
    if(is_plastic == choosePlastic):
        print("Good choice")
        player.is_good = True
        player.play()
        if(choosePlastic):
            motor.right()
        else:
            motor.left()
    else:
        print("Bad choice")
        player.is_good = False
        player.play()
    print("User choice ended")
    

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

port1 = 6
port2 = 14
IO.setup(port1, IO.IN, pull_up_down=IO.PUD_DOWN)
IO.setup(port2, IO.IN, pull_up_down=IO.PUD_DOWN)

motor = GroveServo(12)

def read_input():
    while True:
        if IO.input(port1) != IO.HIGH:
            return 'recyclable'
        
        elif IO.input(port2) != IO.HIGH:
            return 'not recyclable'
    
    
print("init finished")

while True:
    input = None
    input = read_input()

    print(input)
    if input == 'recyclable':
        moveTrash(model, cam, True)
    if input == 'not recyclable':
        moveTrash(model, cam, False)



