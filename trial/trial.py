import socket
import sys
import os
import json
import io
import threading
import time


s=socket.socket()
s.bind(("", int(60002)))
s.listen(5)
# while len(q)!=0:
send_list=[]

def run_server(port_file):
	count=len(port_file[0])

	cmd=""
	for i in range(0,min(count,4)):
		cmd+=" python server.py "+str(port_file[0][i][0])+" "+str(port_file[0][i][1])+" &"
	cmd=cmd[:-1]
	print(cmd)
	os.system(cmd)
	# send_list=send_list[i:]
	# cmd=cmd[:-1]
	# cmd="python server.py 60002 pics00 & python server.py 60003 pics01"
	# print(cmd)
	return

def run_client(packets,port,ip):
	count=len(packets)
	cmd=""
	for i in range(0,min(count,4)):
		cmd+=" python client.py "+str(packets[i])+" "+str(port[i])+" "+str(ip)+" &"
	cmd=cmd[:-1]
	print(cmd)
	os.system(cmd)

	# cmd=cmd[:-1]
	return
def _json_decode(json_bytes):
	tiow = io.TextIOWrapper(
	    io.BytesIO(json_bytes), encoding="utf-8", newline=""
	)
	obj = json.load(tiow)
	tiow.close()
	return obj

def _json_encode(obj):
	return json.dumps(obj, ensure_ascii=False).encode("utf-8")

def list_free_ports(n):								#x=256=> free
	free_list=[]
	i=60003
	count=0
	while count!=n:
		command="netstat -antu | grep "+str(i)
		x=os.system(command)
		print(x,i)
		if x==256:
			free_list.append(i)
			count+=1
		i+=1
	return free_list
# print(free)

def process_message(data):
	task=data.get("task")
	if(task=="send"):
		fname=data.get("fname")
		packets=data.get("packets")
		size=data.get("size")
		return task,fname,packets,size
	if(task=="receive"):
		ports=data.get("ports")
		packets=data.get("packets")
		return task,ports,packets

def send_ack(ip,packets):
	s1=socket.socket()
	s1.connect((str(ip),60001))
	freeports=list_free_ports(len(packets))
	port_file=[]
	for i in range(0,len(packets)):
		a=(freeports[i],packets[i])
		port_file.append(a)
	s1.send(_json_encode({"task":'receive',"ports":freeports,"packets":packets}))
	s1.close()
	return port_file


while True:
	conn, addr = s.accept()     # Establish connection with client.
	print ('Got connection from', addr)
	data = conn.recv(4096)
	# for x in data:
	# 	y=x.split(" ")
	data=_json_decode(data)
	print(repr(data))
	# for i in data:
		# print(i,data.get(i))
	task=data.get("task")
	# task,fname,packets,size=process_message(data)
	if(task=="send"):
		try:
			task,fname,packets,size=process_message(data)
			send_list.append(send_ack(addr[0],packets))			#write fn to send packets

			thread1=threading.Thread(target=run_server, args=(send_list,))
			thread1.start()
			send_list=send_list[4:]
		except socket.error:
			print('error')
	if(task=="receive"):
		try:
			task,ports,packets=process_message(data)
			time.sleep(0.5)
			thread2=threading.Thread(target=run_client, args=(packets,ports,addr[0],))
			thread2.start()
			# fn for listening on the ports
		except socket.error:
			print("error")
	# free=list_free_ports(len(data.get()))
	# try:
	# 	s1=socket.socket()
	# 	s1.connect((addr,60000))
	# 	s1.send(_json_encode({"ports"}))

######################################### free ports




##################################
