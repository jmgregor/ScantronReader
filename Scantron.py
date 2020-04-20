# -*- coding: utf-8 -*-
"""
Project: Scantron Reader
File: scantronReader.py
Authors: Jared Gregor and Aidan Herbert
Date: April 2020

Description:
    The goals of this project are to read in filled out bubble sheets and 
    return a CSV containing grades. The following code works with scanned 
    documents in PDF format.
    
"""
##import libraries
import csv
import cv2
import sys
import os
import math
import numpy as np
from os import path
from pdf2image import convert_from_path

def ScantronGrades(filename):
    ##check filename
    if(str(path.exists(filename))=="False"):
        sys.exit("File does not exist. Try a different path.")
        
    ##Read in PDF
    images = convert_from_path(filename)
    
    ##read in blank scantron
    blank = cv2.imread('test_documents/blank_scantron.png',0)
    cBlank = cv2.cvtColor(blank,cv2.COLOR_GRAY2BGR)
    #get blank pTransform points
    #endPts = pTransformCoords(blank)
    
    ##prepare CSV with header
    csv_data = [["Last Name","First Name","University ID","Additional Info","Percentage Correct"]]
    
    # EMPTY LISTS
    last = []
    first = []
    UID = []
    additional = []
    answers = []
    #answers_key = []
    
    ##Loop through each page in PDF
    for i, image in enumerate(images):
        # READ IN AS IMAGE FOR OPENCV
        image.save('image.png', "PNG")
        img = cv2.imread('image.png',0)
        bimg = cBlank.copy()

        # PERSPECTIVE TRANSFORM of the image to overlay on blank
        # startPts = pTransformCoords(img)
        
        # matrix = cv2.getAffineTransform(startPts, endPts) 
        # imgTransformed = cv2.warpAffine(img, matrix, (blank.shape[1],blank.shape[0]))        
        
        # matrix = cv2.getPerspectiveTransform(startPts, endPts) 
        # imgTransformed = cv2.warpPerspective(img, matrix, (blank.shape[1],blank.shape[0]))
        
        # PREPROCESSING 
        # otsu --> blur --> 3 channel
        ret, otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
        blur = cv2.GaussianBlur(otsu,(15,15),0)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        # HOUGH CIRCLES
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                  param1=50,param2=30,minRadius=8,maxRadius=30)
        circles = np.uint16(np.around(circles))
        
         
        circlesBlank = cv2.HoughCircles(blank,cv2.HOUGH_GRADIENT,1,20,
                                  param1=50,param2=30,minRadius=8,maxRadius=30)
        circlesBlank = np.uint16(np.around(circles))
        
        #print(circles[0])
        lis = circles[0,:]
        circles_sorted = sorted(lis, key=lambda x: (x[0],x[1]))
        
        # SAVE KEY
        if (i==0):
            key = circles_sorted.copy()  
            
        numbers = 0
        
        #FIND FILLED BUBBLES
        for j in circles[0,:]:
            #get ave pix in circle        
            csum = 0
            pixels = 0                
            for r in range(j[1]-j[2], j[1]+j[2]):
                for c in range(j[0]-j[2], j[0]+j[2]):
                    dist = math.sqrt((r-j[1])**2 + (c-j[0])**2)
                        #print("---------")
                        #print(dist)
                        #print(j[2])
                    if(dist <= j[2]):
                        csum = csum + blur[r,c]
                        pixels = pixels + 1
            ave = csum / pixels
            
            
            # print("\n\nUnsorted=\t", j[0], j[1],j[2])
            # print("Sorted=\t\t",circles_sorted[numbers][0],circles_sorted[numbers][1],circles_sorted[numbers][2])
            # print("Key=\t\t",key[numbers][0],key[numbers][1],key[numbers][2])
            
            # draw the outer circle
            if (ave<150):
                cv2.circle(bimg,(j[0],j[1]),3,(0,255,0),2)

            else:
                cv2.circle(bimg,(j[0],j[1]),2,(255,0,0),2)
                
            numbers=numbers+1
    
        #SHOW CURRENT SHEET            
        cv2.namedWindow('Scantron', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Scantron', 720, 980)
        cv2.imshow('Scantron',bimg)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()
        

        
    
    ##Push data to CSV
    for idx in range(len(last)):
        csv_data.append([last[idx],first[idx],UID[idx],additional[idx],answers[idx]])
    
    ##Output CSV
    with open('gradedScantrons.csv', 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(csv_data)
        
    ##remove temp image file
    os.remove('image.png')
    
def pTransformCoords(img):
    #FIND UPPER LEFT BUBBLE
    crop = img[0:300,0:300]
    circles = cv2.HoughCircles(crop,cv2.HOUGH_GRADIENT,1,20,
                                 param1=50,param2=30,minRadius=8,maxRadius=15)
    circles = np.uint16(np.around(circles))    
    tot = 10000000
    for j in circles[0,:]:
        if(j[0]+j[1] < tot):
            tot = j[0]+j[1]
            r0 = j[0]
            c0 = j[1]

    #FIND 3 TARGETS
    circles2 = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                 param1=50,param2=30,minRadius=30,maxRadius=50)   
    circles2 = np.uint16(np.around(circles2))
    bigCircles = [[0,0,0]]
    for j in circles2[0,:]:
        if ((j[0] > int(0.75 * img.shape[1])) or (j[1] > int(0.75 * img.shape[0]))):
            #Make sure targets outside of bubble area 
            inside = 0
            for b in range(len(bigCircles)):
                #Make sure no duplicate targets
                if ((j[1] < bigCircles[b][0] + 30 and j[1] > bigCircles[b][0] - 30) and (j[0] < bigCircles[b][1] + 30 and j[0] > bigCircles[b][1] - 30)):
                    inside = 1
            if(inside == 0):
                bigCircles.append([j[1],j[0],math.sqrt((j[1]**2)+(j[0]**2))])
                
    #SORT THE LIST [TL, BL, TR, BR] order
    bigCirclesSorted = sorted(bigCircles, key=lambda x: (x[2]))
    for el in bigCirclesSorted:
        el.pop(2)
    bigCirclesSorted[1], bigCirclesSorted[2] = bigCirclesSorted[2], bigCirclesSorted[1]
    bigCirclesSorted[0] = [r0,c0]
    
    
    bigCirclesSorted.pop(2)
    #RETURN as np array for cv2.getPerspectiveTransform
    return np.float32(bigCirclesSorted)
    
##prompt for filename of scantron pdf
#filename = input("Please enter the filename :  ")
filename = "test_documents/filled_scantron.pdf"

ScantronGrades(filename)