import cv2 as cv
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('..\Models\model_40x40.hdf5')
IMG_WIDTH = IMG_HEIGHT = 750

def biggestContour(contours):
    """Finds the biggest contour in the image"""
    max_area = 0
    for contour in contours:
        area = cv.contourArea(contour)
        perimeter = cv.arcLength(contour, True)
        vertices = cv.approxPolyDP(contour, 0.02*perimeter, True)
        if area > max_area and len(vertices == 4):
            max_area = area
            biggest = vertices
    return biggest

def getBinary(img, biggest):
#     peri = cv.arcLength(biggest, True)
#     approx = cv.approxPolyDP(biggest, 0.02*peri, True)
    ax = biggest[0][0]
    ay = biggest[1][0]
    bx = biggest[2][0]
    by = biggest[3][0]
    cx = biggest[4][0]
    cy = biggest[5][0]
    dx = biggest[6][0]
    dy = biggest[7][0]

    width, height = IMG_WIDTH, IMG_HEIGHT
    pts1 = np.float32([[ax, ay], [bx, by], [cx, cy], [dx, dy]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_perspective = cv.warpPerspective(img, matrix, (width, height))
    img_corners = cv.cvtColor(img_perspective, cv.COLOR_BGR2GRAY)

    thresh, img_binary = cv.threshold(img_corners, 125, 255, cv.THRESH_BINARY)
    return img_binary, pts1, pts2

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew

def identifyDigit(img, img_cropped):
#     print(cv.countNonZero(img))
    """Identifies the digit from the cropped image"""
    if cv.countNonZero(img_cropped) > 1550:
        return 0
    else:
        return model.predict(np.array(img).reshape(1, 40, 40,1)).argmax() 

def img2grid(img_binary, grid):
    """Converts the image to a sudoku grid"""
    side = 8
    for i in range (9):
        for j in range (9):
            img_cropped = img_binary[int(i*IMG_WIDTH/9 + side):int(i*IMG_WIDTH/9 + IMG_WIDTH/9 - side), int(j*IMG_WIDTH/9 + side): int(j*IMG_WIDTH/9 + IMG_WIDTH/9 - side)]
            img_cropped = cv.resize(img_cropped, (40, 40))
            grid[i][j] = identifyDigit(img_cropped, cv.erode(img_cropped, np.ones((1, 1),np.uint8), iterations = 1))
    return

def showAnswer(grid, color = (0, 102, 0)):
    imgSolved = np.zeros((IMG_WIDTH, IMG_HEIGHT, 3))
    side = 20
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                cv.putText(imgSolved, str(int(grid[i][j])), 
                           (int(j*IMG_WIDTH/9 + side), int((i+1)*IMG_WIDTH/9 - side)), 
                           cv.FONT_HERSHEY_SIMPLEX, 2.1, color, 3)
    for i in range(10):
        cv.line(imgSolved, (int(i*IMG_WIDTH/9), 0), (int(i*IMG_WIDTH/9), IMG_WIDTH), color, 5, 1)
        cv.line(imgSolved, (0, int(i*IMG_WIDTH/9)), (IMG_WIDTH, int(i*IMG_WIDTH/9)), color, 5, 1)
    return imgSolved

def overlayAnswer(img, imgSolved, height, width, pts1, pts2):
    matrix = cv.getPerspectiveTransform(pts2, pts1)
    imgPerspective = cv.warpPerspective(imgSolved, matrix, (width, height))
    imgPerspective = np.asarray(imgPerspective, np.uint8)
    imgOverlayed = cv.addWeighted(imgPerspective, 2, img, 0.8, 1)
    return imgOverlayed

