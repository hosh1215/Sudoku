# Sudoku Board Reader
# The purpose of this program is to reduce the friction for inputting sudoku puzzles into my current program.
# Most of this I learned from the website credited below.
# credits: https://data-flair.training/blogs/opencv-sudoku-solver/

import cv2
import imutils
import numpy as np
from tensorflow.keras.models import load_model



# Takes an image as input and finds a sudoku board inside of the image
def find_board(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    cv2.imshow("Contour", newimg)


    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None
    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            location = approx
        break
    result = get_perspective(img, location)
    return result, location

#Takes an image and location of an interesting region and return the only selected region with a perspective transformation
def get_perspective(img, location, height = 900, width = 900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result


# split the board into 81 individual images
def split_boxes(board, height, width):
    rows = np.vsplit(board,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
    for box in cols:
        box = cv2.resize(box, (height, width))/255.0
        cv2.imshow("Splitted block", box)
        cv2.waitKey(50)
        boxes.append(box)
    return boxes


if __name__ == '__main__':
    img = cv2.imread('sudoku.png')
    cv2.imshow('Original', img)
    board, location = find_board(img)
    cv2.imshow("newBoard", board)
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    grayH, grayW = gray.shape
    rois = split_boxes(gray, grayH, grayW)
    rois = np.array(rois).reshape(-1, grayH, grayW, 1)

    # THINGS TO WORK ON NEXT TIME:
    # - Rework the split_boxes function so that there are only 81 images to process
    # - Find an OCR suitable for this application
    # - Use it in a loop to determine the value for each image, add value to a 2D array
    # - return 2D array




    # classes = np.arange(0, 10)
    # model = load_model('model.h5')
    # # get prediction
    # prediction = model.predict(rois)
    # # print(prediction)
    # predicted_numbers = []
    # # get classes from prediction
    # for i in prediction:
    #     index = (np.argmax(i))
    #     predicted_number = classes[index]
    #     predicted_numbers.append(predicted_number)
    # print(predicted_numbers)



# Display image in a window

# Wait for a key press and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
