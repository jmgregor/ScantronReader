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
    global label2
    global label3
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Pdf files", 
                                                        "*.pdf*"), 
                                                       ("all files", 
                                                        "*.*")))   
    print(filename + " loaded.")
    label3 = tk.Label(win,text="Loaded:")
    label3.place(x=0,y=180)  
    label2 = tk.Label(win,text = filename)
    label2.place(x=50,y=180)
    return filename
        
#function to be called when the grading button is pressed
def ComputeGrades(filename):
    print("\nGrading...\n")
    label3.destroy()
    label2.destroy()
    label4 = tk.Label(win,text="Grading...")
    label4.place(x=0,y=180)
    Scantron.ScantronGrades(filename)
    label4.destroy()
    label5 = tk.Label(win,text = "Grading Complete! GradedScantrons.csv created.")
    label5.place(x=0,y=180)
    print("All done. :)")


#create instance of tkinter
win = tk.Tk()

#sets the size of the window
win.geometry("400x200")

photo = tk.PhotoImage(file=r"logo.png")
label = tk.Label(win,image=photo)
label.place(x=40,y=0)

#add a title to the window
win.title("Grading Tool")

#prevents the window from being resized
win.resizable(False,False)   

button1 = tk.Button(win,text="Load Scantrons", bd = 5, activeforeground = "green", activebackground = "lightgrey")
button1.place(x = 70,y = 140)
button1['command'] = BrowseFiles

button2 = tk.Button(win,text="Grade Scantrons",bd = 5, activeforeground = "green", activebackground = "lightgrey")
button2.place(x=220,y=140)
button2['command'] =lambda: ComputeGrades(filename)

#infinite gui main loop
#required for any gui application to work
win.mainloop()

