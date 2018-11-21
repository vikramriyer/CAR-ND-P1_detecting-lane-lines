# **Finding Lane Lines on the Road** 
---
The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

#### Steps in the pipeline
1. Edge Detection (Canny)
    a. Convert to gray scale image
    The gray scale image is obtained by used weighted average intensities of R, G and B. This way, the edges become more visible and hence preferred over a color image. While there are other reasons as well, like complexity of the processing is considerably reduced in case of gray scale images. There are few reasons why we convert an image to gray scale before processing.
    
    b. Smoothing using the gaussian
    Images usually tend to have noise and it is a good strategy to smooth them using some form of filters. The Gaussian filter helps is reducing the spurious points. After looking at the images and videos, the noises were not that evident to the naked eye, so assumming that the noises will be small changes in the original pixel values, using a gaussian was a natural choice. It is also a known fact that a histogram of small distortions shows a normal distribution and hence a Gaussian/Normal filter works.
    
    c. Canny edge detection
    Using the smoothed image, the edge pixels in the data are found. There are 2 parameters used in the canny algorithm. 
    1. Low threshold: All the pixels having a threshold lesser than this are not considered
    2. High threshold: All the pixels having a threshold higher than this qualify as edge pixel
    The ones having value between the above 2 are considered of they are connected to a strong edge pixel.
    
2. Hough Transform
    The edge pixels obtained from the Edge detection pipeline are then passed on to the hough space. Now, the points/pixels in the image space ( y = mx + b ) are transformed to lines in the hough space ( b = (-x)m + y ). Now, due to the nature of the algorithm to find the slope and intercept in the polar coordinates, the undefined condition is avoided and the grids points (m,b) having the most number of votes having a value greater than the threshold are returned and these points in the hough space get converted as lines in the image space and qualify as edges.

#### Modifying the draw_lines() function.

### 2. Identify potential shortcomings with your current pipeline
    I will describe the main points that can be considered shortcomings of the project
    1. Parameters:
      There were so many parameters to tune and one had to regressively run and check whether the desired output was obtained. Though the parameters were intuitive, a lot of them were hardcoded so as to entertain the edges in the region of interest.
      The perspective used was that of a drivers. Though this is good to get started, a camera or sensor might be mounted somewhere else and this might create problems to the hardcoded region of interest.
    2. Over fitting:
      Since so many parameters were selected manually, there is a high probability that the (hyper) parameters chosen could over fit the current video. Changes to the image's features like intensity, time of the day, luminosity, etc could highly alter the way the current algorithm works
### 3. Suggest possible improvements to your pipeline
    Learning the parameters using a auto-regressive method could be very helpful. A neural network might learn these (hyper) parameters better. 
    The case I mentioned about the current model (manual) over fitting could be reduced if a neural network is used. A train-test-validation split of the data before publishing the results could probably improve the current accuracy. But again, the traditional computer vision only method might prove to be very costly in terms of time consumption. 
