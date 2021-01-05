from utils import *
from sudoku_solver import *

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from keras.models import load_model

grid = np.ones((9,9))

try:
    img = cv.imread(r'..\test\3.png')
    height, width, _ = img.shape
    img = cv.resize(img, (IMG_WIDTH, IMG_HEIGHT))
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray,(5, 5), 3)
    imgThreshold = cv.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    img_contours = img.copy()
except:
    print('File Not Found')

try:
    img_big_contours = img.copy()
    contours, hierarchy = cv.findContours(imgThreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_contours, contours, -1, (0, 255, 0), 3)

    biggest = biggestContour(contours)
    cv.drawContours(img_big_contours, biggest, -1, (0, 255, 0), 1)
    biggest = np.array(reorder(biggest)).reshape(8,1)    
    imgBinary, pts1, pts2 = getBinary(img, biggest)


    kernel = np.ones((6, 6),np.uint8)
    imgBinary = cv.morphologyEx(imgBinary,cv.MORPH_OPEN, kernel)

    img2grid(imgBinary, grid)
    mask = np.where(grid == 0, 1, 0)

    if solveSudoku(grid):
        imgSolved = showAnswer(mask * grid)
        imgOverlayed = overlayAnswer(img, imgSolved, IMG_WIDTH, IMG_HEIGHT, pts1, pts2)

    else:
        print('Sudoku Not Solvable')
        print(grid)
    cv.imshow('Answer', cv.resize(imgOverlayed, ((int(height/width*512), 512)) if width<height else (int(width/height*512), 512)))
    cv.waitKey(10000)
    cv.destroyAllWindows()
    print('Sudoku Solved')
except:
    print('No Grid Detected')