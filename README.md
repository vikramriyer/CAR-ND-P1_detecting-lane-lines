# **Finding Lane Lines on the Road** 
---
The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

#### Steps in the pipeline
1. Convert to gray scale image
    The gray scale image is obtained by used weighted average intensities of R, G and B. This way, the edges become more visible and hence preferred over a color image. While there are other reasons as well, like complexity of the processing is considerably reduced in case of gray scale images. There are few reasons why we convert an image to gray scale before processing.
    
2. Smoothing using the gaussian
    Images usually tend to have noise and it is a good strategy to smooth them using some form of filters. The Gaussian filter helps is reducing the spurious points. After looking at the images and videos, the noises were not that evident to the naked eye, so assumming that the noises will be small changes in the original pixel values, using a gaussian was a natural choice. It is also a known fact that a histogram of small distortions shows a normal distribution and hence a Gaussian/Normal filter works.
3. Run a canny edge detection
    Set the lower and upper bounds/threshold
4. Region of interest filter mask
5. Run a hough transform
    set rho, theta, threshold, min_line_len, max_line_len parameters

#### Modifying the draw_lines() function.

### 2. Identify potential shortcomings with your current pipeline

### 3. Suggest possible improvements to your pipeline

