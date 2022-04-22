#motor module
import RPi.GPIO as GPIO          
from time import sleep
from time import time
from datetime import timedelta
import socket
from socket import SHUT_RDWR
import os

in3 = 24
in4 = 23
enB = 25
in1 = 17
in2 = 27
enA = 22
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
pA=GPIO.PWM(enA,1000)
pB=GPIO.PWM(enB,1000)

pA.start(50)
pB.start(44)

curr_position = "left"


#Lane detection code
from typing import Sequence
from PIL.Image import WEB
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from numpy.lib.function_base import angle
import math
import colorsys

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

def lanesDetection(img):
    #converting to RGB from traditional BGR color scheme of CV
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    #flipping image for easier image manipulation with cv
    # img = cv.flip(img, 0)

    #Finding height and width of image
    height = img.shape[0]
    width = img.shape[1]

#     plt.imshow(img)
#     plt.ylim(0,height)
#     plt.show()

    #Setting range of colors for white lane
    light_white = (255,255,255)
    dark_white = (160,160,160)

    #Setting range of colors for yellow lane
    light_yellow = (200,230,90)
    dark_yellow = (100,90,10)
#     light_yellow = (180,180,120)
#     dark_yellow = (120,120,0)

    #Extracting mask of white and yellow lanes
    white_mask = cv.inRange(img, dark_white, light_white)
    yellow_mask = cv.inRange(img, dark_yellow, light_yellow)

    #Combining white and yellow lane masks
    lanes_mask = cv.bitwise_or(white_mask, yellow_mask)

    #Using the combined mask on the picture to extract lane image
    lanes_pic = cv.bitwise_and(img, img, mask=yellow_mask)

    
    #Setting a region of interest based on camera calibration
    region_of_interest_vertices = [
        (0, 0), (0,0), (0, height), (width, height), (width, 0), (width, 0)
    ]
    
    #Converting the lane picture to grayscale
    gray_img = cv.cvtColor(lanes_pic, cv.COLOR_RGB2GRAY)
    

#     plt.imshow(gray_img, cmap="gray")
#     plt.ylim(0,height)
#     plt.show()

    #Extracting edges with Canny Edge Detector
    edge = cv.Canny(gray_img, 200, 300, apertureSize=3)
    
    #Cropping the image with edges from Canny Edge Detector
    cropped_image = region_of_interest(
        edge, np.array([region_of_interest_vertices], np.int32))

#     plt.imshow(edge, cmap="gray", vmin=0, vmax=255)
#     plt.ylim(0,height)
#     plt.show()

#     persp = cv.getPerspectiveTransform(np.float32( [ [0,200], [120,280], [190,280], [100,200] ] ),   np.float32( [ [0,0],[0,height],[width,height],[width,0] ] ))
#     cropped_with_lines = cv.warpPerspective(gray_img, persp, (width, height), flags=cv.INTER_LINEAR)
# 
# 
#     right = np.sum(cropped_with_lines[200:340])
#     left = np.sum(cropped_with_lines[340:480])
#     
#     left = left/1000
#     right = right/1000

    print(np.sum(gray_img[260:290, 420:600]))


    if (np.sum(gray_img[260:290, 420:600]) < 50000):
        return "right"
                   
#     if (left - right) > 1000:
#         return "left"
#     
#     elif (right - left) > 1000:
#         return "right"
    
#     elif (right + left) < 500:
#         print("condition")
#         return "right"
          
    else:
        return "straight"


#     plt.imshow(cropped_with_lines, cmap="gray", vmin=0, vmax=255)
#     plt.ylim(0,height)
#     plt.show()

    #Plotting lines over the road lanes through Hough Transformation
    lines = cv.HoughLinesP(cropped_image, cv.HOUGH_PROBABILISTIC, theta=np.pi/180,
                           threshold=20, lines=np.array([]), minLineLength=100, maxLineGap=100)

    
    #Plotting the image with lines
    
    
    
    image_with_lines = draw_lines(img, lines)
    
    img_with_error = cv.line(image_with_lines, (50, 200), (150,200), (0,255,0), 9) 
    
#     plt.imshow(image_with_lines)
#     plt.ylim(0,height)
#     plt.show()
    return image_with_lines


def region_of_interest(img, vertices):
    #Making all pixels outside of Region of Interest black
    mask = np.zeros_like(img)
    match_mask_color = (255)
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv.bitwise_and(img, mask)

    return masked_image


def draw_lines(img, lines):
    #drawing lines extracted from Hough Transformation
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)


    for line in lines:
        for x1, y1, x2, y2 in line:
            cv.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), 2)


    img = cv.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img


def turn_decision(direction):
    if direction == "straight":
        print(direction)
        pA.ChangeDutyCycle(30)# + 30)
        pB.ChangeDutyCycle(28)# + 27)
        
    elif direction == "right":
        print(direction)
        pA.ChangeDutyCycle(30)#+ 30)
        pB.ChangeDutyCycle(32)#+ 30)
        
    elif direction == "left":
        print(direction)
        pA.ChangeDutyCycle(37)#+ 36)
        pB.ChangeDutyCycle(27)#+ 30)
        
def change_lane():
    global curr_position
    change_start = time.time()
    
    print(curr_position)
    
    while(1):
        
        if (curr_position == "l"):
            
            if (time.time()-change_start < 3):
                pA.ChangeDutyCycle(30)#+ 30)
                pB.ChangeDutyCycle(44)#+ 30)
        
            elif (time.time()-change_start < 6):
                pA.ChangeDutyCycle(44)#+ 36)
                pB.ChangeDutyCycle(27)#+ 30)
                
            else:
                curr_position = "r"
                break
        
        elif (curr_position == "r"):
            
            if (time.time()-change_start < 3.5):
                pA.ChangeDutyCycle(47)#+ 36)
                pB.ChangeDutyCycle(27)#+ 30)
                
        
            elif (time.time()-change_start < 7):
                pA.ChangeDutyCycle(30)#+ 30)
                pB.ChangeDutyCycle(40)#+ 30)
                
            else:
                curr_position = "left"
                break
        
        

def start_car():
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    
def stop_car():
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)


# if __name__ == "__main__":

curr_position = input("pos?")
    
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.brightness = 55
camera.contrast = 20
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(2)

serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('192.168.100.9',4020))#Server address i.e home = 192.168.100.8 #hotspot = 192.168.246.84
serverSocket.listen(5)
conn, addr = serverSocket.accept()
conn.setblocking(0)

start = time.time()

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
        img = frame.array
        
        try:
            data=conn.recv(1000).decode()
            print ("Received Input is: "+str(data))
            if data=='e':
                print(data)
                conn.close()
                serverSocket.close()
                GPIO.cleanup()
                break
            
            elif data =='0' or data =='7':
                start_car()
                
            elif data =='1' or data =='8':
                stop_car()
                
            elif data =='2' or data =='9':
                change_lane()
        
        except KeyboardInterrupt:
            rawCapture.truncate(0)
            GPIO.cleanup()
            break
        
        except:
            
            
            
            
            turn_decision(lanesDetection(img))
            key = cv.waitKey(1) & 0xFF

        rawCapture.truncate(0)
            
    #         if (time.time() - start > 0.5):
    #             change_lane()
    #             GPIO.cleanup()
    #             break
                
            


    #     img = cv.imread("road_right.jpg")
    #     lanesDetection(img
except KeyboardInterrupt:
    GPIO.cleanup()

except:
    GPIO.cleanup()
    

print('end')

        