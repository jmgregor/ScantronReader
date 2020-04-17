# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:11:22 2020

@author: Aidan Herbert and Jared Gregor
"""
#inport stuff goes here
import tkinter as tk
from tkinter import filedialog

import Scantron

def BrowseFiles(): 
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Pdf files", 
                                                        "*.pdf*"), 
                                                       ("all files", 
                                                        "*.*")))   
    print(filename + " loaded.")
    return filename
        
#function to be called when the grading button is pressed
def ComputeGrades(filename):
    print("\nGrading...\n")
    Scantron.ScantronGrades(filename)
    print("All done. :)")


#create instance of tkinter
win = tk.Tk()

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
button2['command'] =lambda: ComputeGrades(filename)



#infinite gui main loop
#required for any gui application to work
win.mainloop()

