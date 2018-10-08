import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def undistorte_img(img):
    with open('./camera_cal/dict_pickle.p', mode='rb') as f:
        coefficient = pickle.load(f)
    mtx = coefficient['mtx']
    dist = coefficient['dist']
    dst = cv2.undistort(img, mtx, dist, None, mtx)
    return dst


def abs_sobel_thresh(gray_img, orient='x', kernel=3, thresh=(0, 255), output_abs_s=False):
    # take the derivative in 'x' or 'y' -> vertical or horizontal
    sobel = cv2.Sobel(gray_img, cv2.CV_64F, orient == 'x', orient == 'y', ksize=kernel)
    # take the absolute of derivative value
    abs_sobel = np.absolute(sobel)
    # scale to 8-bit (0-255) then covert to np.uint8
    scale_s = np.uint8(255 * abs_sobel / np.max(abs_sobel))

    grad_binary = np.zeros_like(scale_s)
    grad_binary[(scale_s >= thresh[0]) & (scale_s <= thresh[1])] = 1

    if output_abs_s == True:
        output = abs_sobel
    else:
        output = grad_binary
    return output


def color_thresh(image, s_thresh=(0, 255), v_thresh=(0, 255)):
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    s_ch = hls[:, :, 2]
    s_binary = np.zeros_like(s_ch)
    v_ch = hsv[:, :, 2]
    v_binary = np.zeros_like(v_ch)

    s_binary[(s_ch >= s_thresh[0]) & (s_ch < s_thresh[1])] = 1
    v_binary[(v_ch >= v_thresh[0]) & (v_ch < v_thresh[1])] = 1

    result = np.zeros_like(s_binary)
    result[(s_binary == 1) & (v_binary) == 1] = 1
    return result


def combine_img(img1, img2, cal='and'):
    output = np.zeros_like(img1)
    if cal == 'and':
        output[(img1 == 1) & (img2 == 1)] = 1
    else:
        output[(img1 == 1) | (img2 == 1)] = 1
    return output


def warped_img(image, src, dst):
    img_size = (image.shape[1], image.shape[0])
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    warped = cv2.warpPerspective(image, M, img_size, flags=cv2.INTER_LINEAR)
    return warped, Minv
