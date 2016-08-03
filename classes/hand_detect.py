import cv2
import numpy as np
import math


def detect_hand(img, hand_pos):
    '''
    detect hand using opencv convex hull
    :param img:
    :param hand_pos:
    :return:
    '''
    cv2.rectangle(img, (hand_pos[2], hand_pos[3]), (hand_pos[0], hand_pos[1]), (0, 255, 0), 0)
    crop_img = img[hand_pos[1]:hand_pos[3], hand_pos[0]:hand_pos[2]]
    # find the maximum defect
    grey_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(grey_img, ksize=(21, 21), sigmaX=0)
    _, thresh_img = cv2.threshold(blurred_img, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    max_area = -1
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            ci = i
    cnt = contours[ci]
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
    hull = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh_img, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0, 0, 255], -1)
        cv2.line(crop_img, start, end, [0, 255, 0], 2)

    cv2.namedWindow('Gesture')
    cv2.moveWindow('Gesture', 1000, 110)
    cv2.namedWindow('Hand')
    cv2.moveWindow('Hand', 1000, 100-crop_img.shape[1])
    cv2.namedWindow('Thresholded')
    cv2.moveWindow('Thresholded', 1000 + crop_img.shape[0], 100-crop_img.shape[1])

    cv2.imshow('Gesture', img)
    cv2.imshow('Hand', crop_img)
    cv2.imshow('Thresholded', thresh_img)
    print(count_defects)

    return count_defects

