import progress
from tkinter import *
from tkinter.ttk import *
import time
import os
import threading


def search():
    root.destroy()
    comm = "python3 try.py "+ sys.argv[1]
    os.system(comm)

def keepalive():
    comm = "python3 c1.py " + sys.argv[1]+ " 60000 alive 1"
    print(comm)
    os.system(comm)
download_thread = threading.Thread(target=keepalive)
download_thread.start()
root = Tk()
canvas = Canvas(root, width = 300, height = 300)
canvas.grid(row = 0,columnspan = 2,column =0,rowspan = 2, padx = 10,pady =10)
img = PhotoImage(file="ana.png")
canvas.create_image(20, 20, anchor=NW, image=img)
Button(root, text = 'Start Searching',width=20, command = search).grid(row = 2,columnspan = 2, padx = 40,pady =10)

time.sleep(3)
root.mainloop()
