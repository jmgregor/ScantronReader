# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:11:22 2020

@author: Aidan Herbert
"""

import scantronReader
#inport stuff goes here
import tkinter as tk
from tkinter import filedialog
#create instance of tkinter
win = tk.Tk()
    
#what is run when the load scantrons button is pressed 
def BrowseFiles(): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Pdf files", 
                                                        "*.pdf*"), 
                                                       ("all files", 
                                                        "*.*")))   
    print(filename)

#function to be called when the grading button is pressed
def ComputeGrades():
    print("this is where the grading coding goes")
    scantronReader.Scantron()
    

#sets the size of the window
win.geometry("300x100")

#add a title to the window
win.title("Grading Tool")

#prevents the window from being resized
win.resizable(False,False)   

button1 = tk.Button(win,text="Load Scantrons", bd = 5, activeforeground = "green", activebackground = "lightgrey")
button1.place(x = 50,y = 50)
button1['command'] = BrowseFiles

button2 = tk.Button(win,text="Grade!",bd = 5, activeforeground = "green", activebackground = "lightgrey")
button2.place(x=200,y=50)
button2['command'] = ComputeGrades


#infinite gui main loop
#required for any gui application to work
win.mainloop()


