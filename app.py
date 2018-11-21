import matplotlib.pyplot as plt
import cv2
import numpy as np

def canny(image):
    # convert to gray scale
    # print(image.size)
    image = np.array(image, dtype=np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # smooth
    kernel_size = 5
    blur = cv2.GaussianBlur(gray, (kernel_size,kernel_size), 0)

    # canny edge detection
    return cv2.Canny(blur, 60, 180)

def region_of_interest(image):
    imshape = image.shape
    bottom_left = (150, imshape[0])
    bottom_right = (imshape[1], imshape[0])
    top_left = ((imshape[1]-40)//2, imshape[1]//3)
    top_right = ((imshape[1]+40)//2, imshape[1]//3)
    polygon = np.array([
        [
            bottom_left,
            top_left,
            top_right,
            bottom_right
        ]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(mask, image)
    return masked_image

def hough(image):
    rho = 2
    theta = np.pi/180
    threshold = 100
    placeholder = np.array([])
    return cv2.HoughLinesP(image, rho, theta, threshold, placeholder, minLineLength=20, maxLineGap=30)

def get_coordinates(image, averages):
    # print(averages.size)
    # print(averages)
    if averages.size == 1:
        return np.array([[870, 540, 517, 324]])
    m, b = averages
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - b)/m)
    x2 = int((y2 - b)/m)
    print([x1, y1, x2, y2])
    return np.array([x1, y1, x2, y2])

def slope_intercept(image, lines):
    if lines is not None:
        left = []
        right = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            # print((x1,x2),(y1,y2), "x1,x2,y1,y2")
            m, b = np.polyfit((x1,x2), (y1,y2), 1)
            # print(m)
            if m < 0:
                # print((m,b))
                left.append((m, b))
            else:
                right.append((m, b))
    left_avg = np.average(left, axis=0)
    right_avg = np.average(right, axis=0)
    # print(left_avg, "left")
    # print(right_avg, "right")

    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    left_line = get_coordinates(image, left_avg)
    right_line = get_coordinates(image, right_avg)
    return np.array([left_line, right_line])

def draw_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), thickness=8)
    return line_image

# read the image
# image = cv2.imread('test_images/solidWhiteCurve.jpg')
# image_copy = np.copy(image)
# canny_image = canny(image)
#
# # set the area of interest
# masked_image = region_of_interest(canny_image)
#
# # hough transform
# lines = hough(masked_image)
#
# # extrapolated
# extrapolated_lines = slope_intercept(image_copy, lines)
#
# # draw the lines
# line_image = draw_lines(image_copy, extrapolated_lines)
#
# # weighted sum to draw lines onto the original image
# combined = cv2.addWeighted(image_copy, 0.8, line_image, 1, 1)

# display the image
# cv2.imshow('result', combined)
# if cv2.waitKey(0) == 'q':
#     cv2.destroyAllWindows()
#     exit(0)

cap = cv2.VideoCapture('test_videos/solidWhiteRight.mp4') #test_videos/solidWhiteRight.mp4')
while cap.isOpened():
    _, frame = cap.read()

    if not type(frame) is np.ndarray:
        continue
    # cv2.imshow('res', image)

    # image_copy = np.copy(image)
    canny_image = canny(frame)

    # set the area of interest
    cropped_image = region_of_interest(canny_image)

    # hough transform
    lines = hough(cropped_image)

    # extrapolated
    averaged_lines = slope_intercept(frame, lines)

    # draw the lines
    line_image = draw_lines(frame, averaged_lines)

    # weighted sum to draw lines onto the original image
    combined = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow('result', combined)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
