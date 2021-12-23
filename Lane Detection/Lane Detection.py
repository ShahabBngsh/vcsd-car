from typing import Sequence
from PIL.Image import WEB
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from numpy.lib.function_base import angle
import math
import colorsys

def lanesDetection(img):
    #converting to RGB from traditional BGR color scheme of CV
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    #flipping image for easier image manipulation with cv
    img = cv.flip(img, 0)

    #Finding height and width of image
    height = img.shape[0]
    width = img.shape[1]

    plt.imshow(img)
    plt.ylim(0,height)
    plt.show()

    #Setting range of colors for white lane
    light_white = (255,255,255)
    dark_white = (180,180,180)

    #Setting range of colors for yellow lane
    light_yellow = (210,210,150)
    dark_yellow = (150,150,0)

    #Extracting mask of white and yellow lanes
    white_mask = cv.inRange(img, dark_white, light_white)
    yellow_mask = cv.inRange(img, dark_yellow, light_yellow)

    #Combining white and yellow lane masks
    lanes_mask = cv.bitwise_or(white_mask, yellow_mask)

    #Using the combined mask on the picture to extract lane image
    lanes_pic = cv.bitwise_and(img, img, mask=lanes_mask)

    
    #Setting a region of interest based on camera calibration
    region_of_interest_vertices = [
        (0, 300), (0,500), (200, 2*height/3), (width-200, 2*height/3), (width, 500), (width, 300)
    ]
    
    #Converting the lane picture to grayscale
    gray_img = cv.cvtColor(lanes_pic, cv.COLOR_RGB2GRAY)

    plt.imshow(gray_img, cmap="gray")
    plt.ylim(0,height)
    plt.show()

    #Extracting edges with Canny Edge Detector
    edge = cv.Canny(gray_img, 200, 300, apertureSize=3)
    
    #Cropping the image with edges from Canny Edge Detector
    cropped_image = region_of_interest(
        edge, np.array([region_of_interest_vertices], np.int32))

    plt.imshow(edge, cmap="gray", vmin=0, vmax=255)
    plt.ylim(0,height)
    plt.show()

    plt.imshow(cropped_image, cmap="gray", vmin=0, vmax=255)
    plt.ylim(0,height)
    plt.show()

    #Plotting lines over the road lanes through Hough Transformation
    lines = cv.HoughLinesP(cropped_image, cv.HOUGH_PROBABILISTIC, theta=np.pi/180,
                           threshold=20, lines=np.array([]), minLineLength=100, maxLineGap=100)

    
    #Plotting the image with lines
    image_with_lines = draw_lines(img, lines)
    plt.imshow(image_with_lines)
    plt.ylim(0,height)
    plt.show()
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


if __name__ == "__main__":
    #Loading image
    img = cv.imread("C:/Users/Arun-PC/Desktop/PersonalFiles/FYP Project/Lane Detection/left/road_left_1.jpeg")
    

    lanesDetection(img)