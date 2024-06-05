import numpy as np
import cv2


def canny_hough_detect(img: np.ndarray,
                       gaussian_kernel_size: int = 9,
                       canny_thresholds: tuple[int, int] = (200, 250),
                       hough_threshold: int = 25,
                       min_line_length: int = 60,
                       max_line_gap: int = 0) -> np.ndarray:
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    blur = cv2.GaussianBlur(gray, (gaussian_kernel_size, gaussian_kernel_size), 0)
    eq = cv2.equalizeHist(blur)
    edges = cv2.Canny(eq, threshold1=canny_thresholds[0], threshold2=canny_thresholds[1])
    edges = cv2.dilate(edges, np.ones((3, 3)), iterations=1)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    line_image = np.copy(gray) * 0  # creating a blank to draw lines on

    lines = cv2.HoughLinesP(edges, rho, theta, hough_threshold, np.array([]),
                            min_line_length, max_line_gap)
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 1)

    rows, cols = np.indices(line_image.shape)
    has_value = line_image == 255
    has_fifth_index = (rows % 10 == 0) | (cols % 10 == 0)
    keypoints = np.flip(np.column_stack(np.where(has_value & has_fifth_index)))

    return keypoints
