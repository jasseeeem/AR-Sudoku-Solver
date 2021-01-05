# AR-Sudoku-Solver

This python program takes in an image, solves the sudoku and overlays the answer on the image. 
<p align="center">
  <img src="https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/rm_1.png" height ="300">
</p>
## How does it work?

First step is to preprocess the image. The image is resized, converted to grayscale, blurred a bit and an adaptive threshold is applied to get the contours in the image. Then the contour with the maximum area is found whose corners are marked in light green colour here.
<p align="center">
  <img src="https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/rm_2.png" height ="300">
</p>
Then the corners of the biggest contour is used to do a warp transformation to get the square image of the grid, which is converted to a binary image

<p align="center">
  <img src="https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/rm_3.png" height ="300">
</p>
Then the individual cells are extracted from the binary image, and then passed to convolutional neural network which was trained on printed digits (found in folder all_data). 0 is put in the cell if the number of white pixels are greater than a threshold value, and if its lesser the predicted value is put in the cell.
<p align="center">
  <img src="https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/rm_4.png" height ="50">
</p>
The sudoku is solved using a backtracking algorithm and then the 0 values of grid are replaced by the answer. This grid is then masked and the values that should be present in the blank cells are converted to an image. A grid is also added by drawing vertical and horizontal lines. This image is the warp transformed to overlay on top of the original image.
<p align="center">
  <img src="https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/rm_5.png" height ="300">
</p>
This warped image is then overlayed on top of the original image to get the final answer!!!
<p align="center">
  <img src="https://github.com/Jaseem001/AR-Sudoku-Solver/blob/master/test/rm_6.png" height ="300">
</p>
