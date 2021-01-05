# AR-Sudoku-Solver

This python program takes in an image, solves the sudoku and overlays the answer on the image. 

![alt text](https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/readme_1.png?raw=true)

## How does it work?

First step is to preprocess the image. The image is resized, converted to grayscale, blurred a bit and an adaptive threshold is applied to get the contours in the image. Then the contour with the maximum area is found whose corners are marked in light green colour here.
![alt text](https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/readme_2.png?raw=true)

Then the corners of the biggest contour is used to do a warp transformation to get the square image of the grid, which is converted to a binary image

![alt text](https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/readme_3.png?raw=true)

Then the individual cells are extracted from the binary image, and then passed to convolutional neural network which was trained on printed digits (found in folder all_data). 0 is put in the cell if the number of white pixels are greater than a threshold value, and if its lesser the predicted value is put in the cell.

![alt text](https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/readme_4.png?raw=true)

The sudoku is solved using a backtracking algorithm and then the 0 values of grid are replaced by the answer. This grid is then masked and the values that should be present in the blank cells are converted to an image. A grid is also added by drawing vertical and horizontal lines. This image is the warp transformed to overlay on top of the original image.

![alt text](https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/readme_5.png?raw=true)

This warped image is then overlayed on top of the original image to get the final answer!!!

![alt text](https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/readme_6.png?raw=true)
