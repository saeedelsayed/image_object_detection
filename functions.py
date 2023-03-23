import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy import signal

def gaussian_kernel(size, sigma=4):
    size = int(size) // 2
    x, y = np.mgrid[-size:size+1, -size:size+1]
    normal = 1 / (2.0 * np.pi * sigma**2)
    g =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    return g

def sobel_filters(filtered_image):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
    
    Ix = signal.convolve2d(filtered_image, Kx)
    Iy = signal.convolve2d(filtered_image, Ky)
    
    G = np.hypot(Ix, Iy)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)
    
    return G, theta

def non_max_suppression(gradient, direction):
    M, N = gradient.shape
    Z = np.zeros((M,N), dtype=np.int32)
    angle = direction * 180. / np.pi
    angle[angle < 0] += 180

    
    for i in range(1,M-1):
        for j in range(1,N-1):
            try:
                q = 255
                r = 255
                
               #angle 0
                if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                    q = gradient[i, j+1]
                    r = gradient[i, j-1]
                #angle 45
                elif (22.5 <= angle[i,j] < 67.5):
                    q = gradient[i+1, j-1]
                    r = gradient[i-1, j+1]
                #angle 90
                elif (67.5 <= angle[i,j] < 112.5):
                    q = gradient[i+1, j]
                    r = gradient[i-1, j]
                #angle 135
                elif (112.5 <= angle[i,j] < 157.5):
                    q = gradient[i-1, j-1]
                    r = gradient[i+1, j+1]

                if (gradient[i,j] >= q) and (gradient[i,j] >= r):
                    Z[i,j] = gradient[i,j]
                else:
                    Z[i,j] = 0

            except IndexError as e:
                pass
    
    return Z

def threshold(non_maximum_suppression, lowThresholdRatio=0.05, highThresholdRatio=0.2):
    
    highThreshold = non_maximum_suppression.max() * highThresholdRatio;
    lowThreshold = highThreshold * lowThresholdRatio;
    
    M, N = non_maximum_suppression.shape
    res = np.zeros((M,N), dtype=np.int32)
    
    weak = np.int32(25)
    strong = np.int32(255)
    
    strong_i, strong_j = np.where(non_maximum_suppression >= highThreshold)
    zeros_i, zeros_j = np.where(non_maximum_suppression < lowThreshold)
    
    weak_i, weak_j = np.where((non_maximum_suppression <= highThreshold) & (non_maximum_suppression >= lowThreshold))
    
    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak
    
    return res

def hysteresis(double_threshold, weak=25, strong=255):
    M, N = double_threshold.shape  
    for i in range(1, M-1):
        for j in range(1, N-1):
            if (double_threshold[i,j] == weak):
                try:
                    if ((double_threshold[i+1, j-1] == strong) or (double_threshold[i+1, j] == strong) or (double_threshold[i+1, j+1] == strong)
                        or (double_threshold[i, j-1] == strong) or (double_threshold[i, j+1] == strong)
                        or (double_threshold[i-1, j-1] == strong) or (double_threshold[i-1, j] == strong) or (double_threshold[i-1, j+1] == strong)):
                        double_threshold[i, j] = strong
                    else:
                        double_threshold[i, j] = 0
                except IndexError as e:
                    pass
    return double_threshold

def canny_edge_detection(image):
    #noise filter  ----> step one
    filterd_image = signal.convolve2d(image, gaussian_kernel(5))

    #gradient and direction -----> step two
    gradient,theta = sobel_filters(filtered_image=filterd_image)

    #non maximum suppression -----> step three
    non_maximum_suppression = non_max_suppression(gradient=gradient,direction=theta)

    #double threshold ----> step four
    double_threshold = threshold(non_maximum_suppression=non_maximum_suppression)

    #hysteresis ----> step five
    hysteresis_image = hysteresis(double_threshold=double_threshold)

    return hysteresis_image

def hough_line(image,edge):
    row,column = edge.shape
    max_normal = int(np.round(np.sqrt(row**2 + column**2)))
    thetas = np.deg2rad(np.arange(-90, 91))
    r = np.arange(0,max_normal+1)
    accumulator = np.zeros((len(r), len(thetas)))
    for y in range(row):
        for x in range(column):
            if edge[y,x] > 0:
                for k in range(len(thetas)):
                    normal = x * np.cos(thetas[k]) + y * np.sin(thetas[k])
                    accumulator[int(normal),k] += 1

    for i in range(accumulator.shape[0]): # i is r
        for j in range(accumulator.shape[1]): # j is theta
            if(accumulator[i][j] >= 150): # this is line
                if(int(thetas[j])==0):
                    if(r[i] < image.shape[1]):
                        x = r[i]
                        for k in range(image.shape[0]):
                            image[k][x] = 0
                else:
                    for k in range(image.shape[1]):
                        x = k
                        y = (-1 * np.cos(thetas[j]) / np.sin(thetas[j]) * x) + (r[i] / np.sin(thetas[j]))
                        if(y >= 0 and y < image.shape[0]):
                            image[int(y)][x] = 0
    return image 


def hough_circle(image,edge):
    row,column = edge.shape
    max_radius = int(np.round(np.sqrt(row**2 + column**2)))
    accumulator = np.zeros((row,column,max_radius))

    for r in range(0,max_radius):
        for y in range(row):
            for x in range(column):
                if(edge[y,x] > 0):
                    for theta in range(0,361):
                        a = x - r * np.cos(theta * np.pi / 180)
                        b = y - r * np.sin(theta * np.pi / 180)
                        if(a >= 0 and a < column and b >= 0 and b < row):
                            accumulator[int(b)][int(a)][r] += 1

    for b in range(row):
        for a in range(column):
            for r in range(max_radius):
                if(accumulator[b][a][r] >= 200):
                    for x in range(image.shape[1]):
                        temp = r**2 - (x - a)**2
                        if(temp >= 0):
                            y_positive = int(np.sqrt(temp) + b) 
                            y_negative = int(-1 * np.sqrt(temp) + b) 
                            if(y_positive >= 0 and y_positive < image.shape[0] and y_negative >= 0 and y_negative < image.shape[0]):
                                image[y_positive][x] = 0
                                image[y_negative][x] = 0
    return image
