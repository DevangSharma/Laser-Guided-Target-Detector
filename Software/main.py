import numpy as np
import cv2
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)


def left():
    arduino.write(bytes("l", 'utf-8'))
    time.sleep(0.05)


def right():
    arduino.write(bytes("r", 'utf-8'))
    time.sleep(0.05)


def up():
    arduino.write(bytes("u", 'utf-8'))
    time.sleep(0.05)


def down():
    arduino.write(bytes("d", 'utf-8'))
    # time.sleep(0.05)


def target(webcam):
    a = 0
    b = 0
    c = 0
    d = 0
    _, imageFrame = webcam.read()

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

    kernal = np.ones((5, 5), "uint8")

    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                mask=green_mask)

    contours, hierarchy = cv2.findContours(green_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            a, b, c, d = cv2.boundingRect(contour)

    return a, b, c, d


def laser(cap):
    x_min = 0
    y_min = 0
    box_width = 0
    box_height = 0
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if contours:
        (x_min, y_min, box_width, box_height) = cv2.boundingRect(contours[0])

    return x_min, y_min, box_width, box_height


camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    x, y, w, h = laser(camera)

    cv2.rectangle(frame, (x, y),
                               (x + w, y + h),
                               (0, 0, 255), 2)

    cv2.putText(frame, "Laser", (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 0, 255),3)

    a,b,c,d = target(camera)

    cv2.rectangle(frame, (a, b),
                  (a + c, b + d),
                  (0, 255, 0), 2)

    cv2.putText(frame, "Target", (a, b),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 255, 0), 3)

    targetmidx = a + (c//2)
    targetmidy = b + (d//2)

    lasermidx = x + (w//2)
    lasermidy = y + (h//2)

    if(lasermidx < targetmidx):
        print(lasermidx,targetmidx)
        right()
    elif(lasermidx > targetmidx):
        left()

    if (lasermidy < targetmidy):
        down()
    elif (lasermidy > targetmidy):
        up()

    cv2.imshow("Automatic Enemy Striker", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
