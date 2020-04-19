# -*- coding: utf-8 -*-
"""
Project: Scantron Reader
File: scantronReader.py
Authors: Jared Gregor, Aidan Herbert, Gayle McAdams, Dan Mullen, Simon Yahn
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

# def sortSheet(sheet):
#     sortedSheet = sheet.copy()
#     for p in sheet[0,:]:
#         for e in sheet [0,]    

def ScantronGrades(filename):
    ##check filename
    if(str(path.exists(filename))=="False"):
        sys.exit("File does not exist. Try a different path.")
        
    ##Read in PDF
    images = convert_from_path(filename)
    
    ##prepare CSV with header
    csv_data = [["Last Name","First Name","University ID","Additional Info","Percentage Correct"]]
    
    ##create lists to hold info needed
    last = []
    first = []
    UID = []
    additional = []
    answers = []
    #answers_key = []
    
    ##Loop through each page in PDF
    for i, image in enumerate(images):
        ##convert to png for opencv
        image.save('image.png', "PNG")
        img = cv2.imread('image.png',0)

        pTransform(img)

    #     # PREPROCESSING otsu --> blur --> 3 channel
    #     ret, otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
    #     blur = cv2.GaussianBlur(otsu,(15,15),0)
    #     cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    #     # bubbles = cimg[int(cimg.shape[0]/2)-40:,:]
    #     # cv2.imshow('Scantron',bubbles)
    #     # cv2.waitKey(10000)
    #     # cv2.destroyAllWindows()


    #     # HOUGH CIRCLES
    #     circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
    #                              param1=50,param2=30,minRadius=8,maxRadius=30)
    #     circles = np.uint16(np.around(circles))
        
    #     #print(circles[0])
    #     lis = circles[0,:]
    #     circles_sorted = sorted(lis, key=lambda x: (x[0],x[1]))

        
        
    #     # SAVE KEY
    #     if (i==0):
    #         key = circles_sorted.copy()  
            
    #     numbers = 0
        
    #     #Loop all circles and find filled
    #     #filled = []
    #     print("\n\n\nNEW PAGE")
    #     for j in circles[0,:]:
    #         #get ave pix in circle        
    #         csum = 0
    #         pixels = 0                
    #         for r in range(j[1]-j[2], j[1]+j[2]):
    #             for c in range(j[0]-j[2], j[0]+j[2]):
    #                 dist = math.sqrt((r-j[1])**2 + (c-j[0])**2)
    #                     #print("---------")
    #                     #print(dist)
    #                     #print(j[2])
    #                 if(dist <= j[2]):
    #                     csum = csum + blur[r,c]
    #                     pixels = pixels + 1
    #         ave = csum / pixels
            
            
    #         print("\n\nUnsorted=\t", j[0], j[1],j[2])
    #         print("Sorted=\t\t",circles_sorted[numbers][0],circles_sorted[numbers][1],circles_sorted[numbers][2])
    #         print("Key=\t\t",key[numbers][0],key[numbers][1],key[numbers][2])

            
    #         # draw the outer circle
    #         if (ave<150):
    #             if (circles_sorted[numbers][0] <= key[numbers][0] + key[numbers][2] and circles_sorted[numbers][0] >= key[numbers][0] - key[numbers][2] and circles_sorted[numbers][1] <= key[numbers][1] + key[numbers][2] and circles_sorted[numbers][1] >= key[numbers][1] - key[numbers][2]):
    #                 cv2.circle(cimg,(j[0],j[1]),j[2],(0,255,0),2)
    #             else:
    #                 cv2.circle(cimg,(j[0],j[1]),j[2],(0,0,255),2)
    #             #filled.append(j)
    #             #print(ave)
                
    #         else:
    #             cv2.circle(cimg,(j[0],j[1]),2,(255,0,0),2)
    
            
    #         #print(cimg[j[1],j[0]])
            
            

                
    #         numbers=numbers+1
    
    #     #print(numbers)
            
    #     #sort filled bubbles for identification
    #   #  sortSheet(filled)
    

            
    #     cv2.namedWindow('Scantron', cv2.WINDOW_NORMAL)
    #     cv2.resizeWindow('Scantron', 720, 980)
    #     cv2.imshow('Scantron',cimg)
    #     cv2.waitKey(10000)
    #     cv2.destroyAllWindows()
        

        
    
    # ##Push data to CSV
    # for idx in range(len(last)):
    #     csv_data.append([last[idx],first[idx],UID[idx],additional[idx],answers[idx]])
    
    # ##Output CSV
    # with open('gradedScantrons.csv', 'w', newline='') as csv_output:
    #     writer = csv.writer(csv_output)
    #     writer.writerows(csv_data)
        
    # ##remove temp image file
    # os.remove('image.png')
    
    
def pTransform(img):
    pts2=np.float32([[0,0],[img.shape[0],0],[0,img.shape[1]],[img.shape[0],img.shape[1]]])
    
    crop = img[0:2000,0:1500]
    
    circles = cv2.HoughCircles(crop,cv2.HOUGH_GRADIENT,1,20,
                                 param1=50,param2=30,minRadius=8,maxRadius=30)
    circles = np.uint16(np.around(circles))
        
    #print(circles[0])
    lis = circles[0,:]
    circles_sorted = sorted(lis, key=lambda x: (x[0],x[1]))
    
    circles2 = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                 param1=50,param2=30,minRadius=30,maxRadius=50)
    circles2 = np.uint16(np.around(circles2))
    
    
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    cv2.circle(cimg,(circles_sorted[0][0],circles_sorted[0][1]),20,(0,255,0),2)
    cv2.circle(cimg,(circles_sorted[-1][0],circles_sorted[-1][1]),20,(0,255,0),2)    
    for j in circles2[0,:]:
        print(j[2])
        cv2.circle(cimg,(j[0],j[1]),j[2],(0,0,255),2)
        cv2.namedWindow('Scantron', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Scantron', 720, 980)
        cv2.imshow('Scantron',cimg)
        cv2.waitKey(10000)
        cv2.destroyAllWindows()
    
    
##prompt for filename of scantron pdf
#filename = input("Please enter the filename :  ")
filename = "test_documents/filled_scantron.pdf"

ScantronGrades(filename)