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
    correctAns = []
    
    ##Loop through each page in PDF
    for i, image in enumerate(images):
        ##convert to png for opencv
        image.save('image.png', "PNG")
        img = cv2.imread('image.png',0)
        
        # find otsu's threshold value with OpenCV function
        ret, otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
        
        blur = cv2.GaussianBlur(otsu,(15,15),0)
    
        
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                 param1=50,param2=30,minRadius=8,maxRadius=30)
    
        circles = np.uint16(np.around(circles))
        numbers = 0
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
            
            #print(ave)
            
            # draw the outer circle
            if (ave<150):
                cv2.circle(cimg,(j[0],j[1]),j[2],(0,0,255),2)
                #print(ave)
                
            else:
                cv2.circle(cimg,(j[0],j[1]),j[2],(0,255,0),2)
    
            
            #print(cimg[j[1],j[0]])
            
            # draw the center of the circle
            #cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
            numbers=numbers+1
    
        #print(numbers)
    
        cv2.namedWindow('Scantron', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Scantron', 720, 980)
        cv2.imshow('Scantron',cimg)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        
        ##Save Key
        #if (i==0):
            #save key
            #print("KEY")
        
    
    ##Push data to CSV
    for idx in range(len(last)):
        csv_data.append([last[idx],first[idx],UID[idx],additional[idx],correctAns[idx]])
    
    ##Output CSV
    with open('gradedScantrons.csv', 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(csv_data)
        
    ##remove temp image file
    os.remove('image.png')
    
    
##prompt for filename of scantron pdf
#filename = input("Please enter the filename :  ")
#filename = "test_documents/filled_scantron.pdf"

#Scantron(filename)