# **Finding Lane Lines on the Road** 
---
The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflecting the work done in a report

![Lane Line](https://raw.githubusercontent.com/vikramriyer/CAR-ND-P1_detecting-lane-lines/master/test_images_output/solidYellowLeft.jpg)

---

### Reflection

#### Steps in the pipeline
#### 1. Edge Detection (Canny)

##### a. Convert to gray scale image
    
The gray scale image is obtained by used weighted average intensities of R, G and B. This way, the edges become more visible and hence preferred over a color image. While there are other reasons as well, like complexity of the processing is considerably reduced in case of gray scale images. There are few reasons why we convert an image to gray scale before  processing.
    
##### b. Smoothing using the gaussian
    
Images usually tend to have noise and it is a good strategy to smooth them using some form of filters. The Gaussian filter  helps is reducing the spurious points. After looking at the images and videos, the noises were not that evident to the naked eye, so assumming that the noises will be small changes in the original pixel values, using a gaussian was a natural choice. It is also a known fact that a histogram of small distortions shows a normal distribution and hence a Gaussian/Normal filter works.

##### c. Canny edge detection

Using the smoothed image, the edge pixels in the data are found. There are 2 parameters used in the canny algorithm. 
    1. Low threshold: All the pixels having a threshold lesser than this are not considered
    2. High threshold: All the pixels having a threshold higher than this qualify as edge pixel
The ones having value between the above 2 are considered of they are connected to a strong edge pixel.
    
#### 2. Hough Transform
    
The edge pixels obtained from the Edge detection pipeline are then passed on to the hough space. Now, the points/pixels in the image space ( y = mx + b ) are transformed to lines in the hough space ( b = (-x)m + y ). Now, due to the nature of the algorithm to find the slope and intercept in the polar coordinates, the undefined condition incase of a zero slope is avoided. The grid points (m,b) i.e. in the hough space that have the most number of votes are returned back. The important constrain is that they must have a value greater than the threshold. These points in the hough space get converted as lines in the image space and qualify as edges.

#### Modifying the draw_lines() function.

1. Part 1 (partly successful effort)

Initially, the I found out the min and max variables that were possible for x and y at the top and bottom in the region of interest. When run individually, the images showed good results and the time complexity did not seem to bother me much.
However, the slighest of change in the intensities created major issues with this model.

Below is code snippet for the logic
```
class Min_Max_Left:
    min_x, min_y, max_x, max_y = 960 + 10, 540 + 10, 0, 0
    
class Min_Max_Right:
    min_x, min_y, max_x, max_y = 960 + 10, 540 + 10, 0, 0
    
# find the min and max of x and y for left and right lines and draw lines
for i in range(len(left)):
    Min_Max_Left.min_x = min(Min_Max_Left.min_x, left[i][0])
    Min_Max_Left.max_x = max(Min_Max_Left.max_x, left[i][0])
    Min_Max_Left.min_y = min(Min_Max_Left.min_y, left[i][1])
    Min_Max_Left.max_y = max(Min_Max_Left.max_y, left[i][1])
cv2.line(img, (Min_Max_Left.min_x, Min_Max_Left.max_y), (Min_Max_Left.max_x, Min_Max_Left.min_y), color, thickness)

for i in range(len(right)):
    Min_Max_Right.min_x = min(Min_Max_Right.min_x, right[i][0])
    Min_Max_Right.max_x = max(Min_Max_Right.max_x, right[i][0])
    Min_Max_Right.min_y = min(Min_Max_Right.min_y, right[i][1])
    Min_Max_Right.max_y = max(Min_Max_Right.max_y, right[i][1])
cv2.line(img, (Min_Max_Right.min_x, Min_Max_Right.min_y), (Min_Max_Right.max_x, Min_Max_Right.max_y), color, thickness)
```

2. Part 2 (successful effort)

We separate out the left and the right lines and individually before finding the averages by accumulating the recent 10 values of the slopes and intercepts that I gained by fitting all the points using the fitline function. The mandatory videos saw an improvement, however, the challenge video has considerable issues with the current pipeline as well.

As we get the accumulated slopes and intercepts, it is very easy to get the coordinates using the formula of a line in (x,y) space i.e. y = mx + c.

### Potential shortcomings with the current pipeline
I will describe the main points that can be considered shortcomings of the project
 - **Parameters**:
  There were so many parameters to tune and one had to regressively run and check whether the desired output was obtained. Though the parameters were intuitive, a lot of them were hardcoded so as to entertain the edges in the region of interest.
  The perspective used was that of a drivers. Though this is good to get started, a camera or sensor might be mounted somewhere else and this might create problems to the hardcoded region of interest.
 - **Over fitting**:
  Since so many parameters were selected manually, there is a high probability that the (hyper) parameters chosen could over fit the current video. Changes to the image's features like intensity, time of the day, luminosity, etc could highly alter the way the current algorithm works
 - **Curves**:
  We as of now are using straight lines to predict where to drive. If there is a sudden curvature in the road, the robustness of the current algorithm is compromised. Though the lane markings correct themselves when coming onto a straingt road. However, the road only has curves or if driving on a hill, you are sure to drive right into the valley (remember doctor strange??!).
### Possible improvements
- We are currently focusing only on drawing straight lines with a polynomial of degree 1. If we somehow figure out drawing curves, that would make the current algorithm more robust.
- Learning the parameters using a auto-regressive method could be very helpful. A neural network might learn these (hyper) parameters better. 
- The case I mentioned about the current model (manual) over fitting could be reduced if a neural network is used. A train-test validation split of the data before publishing the results could probably improve the current accuracy. But again, the traditional computer vision only method might prove to be very costly in terms of time consumption. 
- A short trial stuff can be to replace gray scale with other workarounds like HSL, HSV, etc. This could possibly ensure not much great results, but might be able to remove the small distortions that happen here and there.
