# importing tkinter module
from tkinter import *
from tkinter.ttk import *
import struct
import sys
# creating tkinter window

class pbar:
# Progress bar widget
	def __init__(self,filesize,master):
		self.root = master
		self.filesize = filesize
		self.value = 0
		self.progress = Progressbar(self.root, orient = HORIZONTAL,
				length = 200, mode = 'determinate')
		self.progress.grid(row = 2,columnspan =2,column =0, pady = 10,padx =10)



# Function responsible for the updation
# of the progress bar value
	def update(self,value):
		import time
		self.progress['value'] = value
		self.root.update_idletasks()
		



# This button will initialize
# the progress bar


# infinite loop
