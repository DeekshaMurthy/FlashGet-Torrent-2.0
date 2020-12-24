import sys
import math
import numpy
import os
import subprocess
from tkinter import *
from tkinter.ttk import *
import time
import datetime
import progress
import socket
import sys
import os
import threading
import json

def contact_sender(ip,port,name,size,packet):
	port=int(port)
	s=socket.socket()
	# try:
	s.connect((ip,port))

	s.send(_json_encode({"task":'send',"fname":name,"size":size, "packets":packet}))			#send ur ip too
	# s.close()
	return 1

def _json_encode(obj):
	return json.dumps(obj, ensure_ascii=False).encode("utf-8")

def list_options(file):
    line =""						#state the text file options
    ip=[]
    filename=[]
    size=[]
    rows=[]
    options=[]
    q_file=open(file,"r")
    for line in q_file:
        fields=line.split("\t")
        # print("rows",fields)
        if len(fields) > 1:
            ip.append(fields[0])
            filename.append(fields[1])
            size.append(fields[2])
            rows.append(fields)
            # print("file",filename)

    # print(options,rows)
    q_file.close()
    return ip,filename,size
def list_files(name):				#list all the packets present in order
	name=name+'*'
	command="find ./trial -name '"+name+"'"
	y=os.popen(command).readlines()
	y=list(y)

	list1=[]
	for i in y:
		frag=i[8:-1]
		list1.append(frag)
	list1.sort()

	return list1

def req_files(q1,name,size):
	digit=len(str(size))
	init_files=list_files(name)
	q=[x for x in q1 if str(x).zfill(2) not in init_files]
	# print(q)
	return q

def search():
	master.destroy()
	comm = "python3 try.py 10.196.8.46"
	os.system(comm)

master = Tk()
labelText = StringVar(master)
Label(master, text="Download speed").grid(row = 0, column = 0,pady = 10,padx =10)
Label(master, textvariable=labelText).grid(row = 0, column = 1,pady = 10,padx =10)


filename = sys.argv[1]

ips,filenames,sizes = list_options("IP_list.txt")
ip = []
individual_queue=[]
size = 0.0
for i in range(0,len(ips)):
	if filenames[i] == filename:
		ip.append(ips[i])
		size = int(float(sizes[i][:-2]))					#total packets
print("IP address having ",filename," of size ",size," are ",ip)

l_len=len(ip)
fragments=math.ceil(size/int(l_len))
q2=list(range(0,size))				#queue of packets
q1=[]
for i in range(0,len(q2)):
	q1.append(filename+"_frag{:02d}".format(i))



for i in range(l_len):
	x=q1[(i*fragments):((i+1)*fragments)]
	individual_queue.append(x)

	#find all files with name pics
# print(y[1])
# q2=[]


h = progress.pbar(size,master)
labelText.set(str(0)+" MB")


t=req_files(q1,filename,size)


h.update((len(q1)-len(t))/len(q1)*100)

master.update()
# master.mainloop()


print("\nStarting to request\n")
count =0
ini= datetime.datetime.now()
while len(t)!=0 and count < 4000:

	count+=1
	ips,filenames,sizes = list_options("IP_list.txt")
	ip = []
	individual_queue=[]
	size = 0.0
	for i in range(0,len(ips)):
		if filenames[i] == filename:
			ip.append(ips[i])
			size = int(float(sizes[i][:-2]))					#total packets



	l_len=len(ip)
	fragments=math.ceil(size/int(l_len))


	t=req_files(q1,filename,size)

	h.update((len(q1)-len(t))/len(q1)*100)
	labelText.set(str((len(q1)-len(t)))+" MB")
	for i in range(l_len):
		x=t[(i*fragments):((i+1)*fragments)]
		individual_queue.append(x)

	#master.destroy()


	# master.mainloop()

	peers=len(ip)
	t1=[]
	for i in range(0,peers):
		th=threading.Thread(target=contact_sender, args=(ip[i],60001,filename,size,individual_queue[i][:4]))
		t1.append(th)
		th.start()
	time.sleep(2)
	master.update()
fin= datetime.datetime.now()
#t
#master.destroy()


Label(master, text="Average speed "+str(size/(fin-ini).total_seconds())).grid(row = 3,column = 0,pady = 10,padx =10)
Button(master, text = "Search again",width=20, command = search).grid(row = 4,columnspan = 2, padx = 40,pady =10)
master.mainloop()
# x=list_files("pics")
# print(x)

#z=[x for x in a if x not in b]
#################################################

# def request(ip,q,port):
# 	w
# 	os.system(client.py)
