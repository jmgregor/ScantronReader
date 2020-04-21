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
    #HOUGH CIRCLES blank
    circlesBlank = cv2.HoughCircles(blank,cv2.HOUGH_GRADIENT,1,20,
                                 param1=50,param2=30,minRadius=10,maxRadius=30)
    circlesBlank = np.uint16(np.around(circlesBlank))    
    
    ##prepare CSV with header
    csv_data = [["Last Name","First Name","University ID","Additional Info","Percentage Correct"]]
    
    pageNum = 1
    
    ##Loop through each page in PDF
    for i, image in enumerate(images):
        # READ IN AS IMAGE FOR OPENCV
        image.save('image.png', "PNG")
        img = cv2.imread('image.png',0)
        bimg = cBlank.copy()
        
        # PREPROCESSING 
        # otsu --> blur --> 3 channel
        ret, otsu = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)    
        blur = cv2.GaussianBlur(otsu,(15,15),0)
        #cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        # HOUGH CIRCLES
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                  param1=50,param2=30,minRadius=10,maxRadius=30)
        circles = np.uint16(np.around(circles))
        
        #FIND FILLED BUBBLES on answer sheets
        for j in circles[0,:]:
            #get ave pix in circle        
            csum = 0
            pixels = 0                
            for r in range(j[1]-j[2], j[1]+j[2]):
                for c in range(j[0]-j[2], j[0]+j[2]):
                    dist = math.sqrt((r-j[1])**2 + (c-j[0])**2)
                    if(dist <= j[2]):
                        csum = csum + blur[r,c]
                        pixels = pixels + 1
            ave = csum / pixels
            
            # draw the outer circle
            if (ave<150):
                k = nearestBlank(circlesBlank, j[0], j[1])
                cv2.circle(bimg,(k[0],k[1]),k[2],(0,255,0),-1)
    
        #LAST NAME
        boxLast=bimg[140:995,201:559]
        last = readBubbles(boxLast, 26, 11, 1)
        
        #FIRST NAME
        boxFirst=bimg[140:996,655:945]
        first = readBubbles(boxFirst, 26, 9, 1)
        
        #UID
        boxUID=bimg[140:465,1029:1320]
        UID = readBubbles(boxUID, 10, 9, 0)
    
        #ADDITONAL INFO
        boxAdd=bimg[605:930,1030:1321]
        additional = readBubbles(boxAdd, 10, 9, 0)

        #GRADING
        boxAns=bimg[1079:1902,201:1452]
        answers = ""
        
        # SAVE KEY
        if (i==0):
            key = []
            sections = 30
            numLetters = 25
            change = 77
            col = 13
            for c in range(0, sections):
                for r in range(0, numLetters):
                    row = int(r* 33 + 13)#(height/2))
                    if (boxAns[row, col, 0] == 0 and boxAns[row, col, 1] == 255 and boxAns[row, col, 2] == 0):
                        key.append([row, col])
                    cv2.circle(boxAns,(col,row),3,(255,0,0),-1)
                if (c%15 == 14):
                    change = 92
                if (c%5 == 4):
                    col = col + change
                else:
                    col = col + 33
        else:
            correctAns = 0
            for el in key:
                row = el[0]
                col = el[1]
                if (boxAns[row, col, 0] == 0 and boxAns[row, col, 1] == 255 and boxAns[row, col, 2] == 0):
                    correctAns = correctAns + 1
            answers = answers + str(round(100*(correctAns/len(key)),2))
        
        #APPEND TO CSV
        csv_data.append([last,first,UID,additional,answers])
        
        print("Page " + str(pageNum) + " completed!")
        pageNum = pageNum + 1
        
        # #SHOW CURRENT SHEET            
        # cv2.namedWindow('Scantron', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Scantron', 720, 980)
        # cv2.imshow('Scantron',boxAns)
        # cv2.waitKey(10000)
        # cv2.destroyAllWindows()        
    
    # SAVE CSV
    with open('gradedScantrons.csv', 'w', newline='') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(csv_data)
    print("\nCSV saved to: gradedScantrons.csv")
    # remove temp image file
    os.remove('image.png')
    
def nearestBlank(blankCircles, current0, current1):
    size = 4
    for j in blankCircles[0,:]:
        #print(current0," ",current1," ", j[0], " ", j[1]," ", j[2])
        if(current0 <= j[0]+(j[2]+size) and current0 >= j[0]-(j[2]+size) and current1 <= j[1]+(j[2]+size) and current1 >= j[1]-(j[2]+size)):
            #print("found")
            return j
            
    return [0,0,0]
           
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

def readBubbles(img, numRows, numCols, letters):
    word = ""
    width = 33 
    height = 33 
    for c in range(0, numCols):
        col = int(c*width + 13)
        for r in range(0, numRows):
            row = int(r* height + 13)
            if (img[row, col, 0] == 0 and img[row, col, 1] == 255 and img[row, col, 2] == 0):
                if (letters == 1):
                    word = word + chr(65 + r)
                else:
                    word = word + str(r)
    return word


#MAIN
# filename = "test_documents/filled_scantron.pdf"

# ScantronGrades(filename)