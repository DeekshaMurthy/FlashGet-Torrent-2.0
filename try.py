import progress
from tkinter import *
from tkinter.ttk import *
import time
import os
import threading

master = Tk()
tkvar = StringVar(master)
load = StringVar(master)

def change_dropdown(*args):

    if not tkvar.get() == "None":
        filename = str(tkvar.get())
        master.destroy()
        cmd = "python3 mid.py " + filename
        print(" File ",filename," has been requested for download")
        os.system(cmd)

def execute(strin):
    comm = "python3 c1.py " + sys.argv[1] + " 60000 search " + strin

    os.system(comm)

def search():
    #time.sleep(1)

    #Label(master, text='results').grid(row=1,pady = 3)


    # Dictionary with options

    #tkvar.set('None') # set the default option
    download_thread = threading.Thread(target=execute, args=[str(e1.get())])
    download_thread.start()
    load.set("Loading")
    time.sleep(1)
    load.set("Search")
    choices = list_options("IP_list.txt")
    popupMenu = OptionMenu(master, tkvar,'None', *choices)
    Label(master, text="Choose a file").grid(row = 1, column = 0,pady = 10,padx =10)
    popupMenu.grid(row = 1, column =1,pady = 10,padx =10)
    tkvar.trace('w', change_dropdown)

def list_options(file):
    line =""						#state the text file options
    ip=[]
    filename=['None']
    size=[]
    rows=[]
    options=[]
    q_file=open(file,"r")
    for line in q_file:
        fields=line.split("\t")

        if len(fields) > 1:
            ip.append(fields[0])
            filename.append(fields[1])
            size.append(fields[2])
            rows.append(fields)


    print("IP List of search items",rows)
    q_file.close()
    return set(filename)



Label(master, text='Search For').grid(row=0,pady = 10,padx =10)
e1 = Entry(master)
e1.grid(row=0, column=1,pady = 3, padx= 10)
load.set("Search")
Button(master, textvariable = load,width=20, command = search).grid(row = 2,columnspan = 2, padx = 40,pady =10)



mainloop()
