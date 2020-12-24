import socket                   # Import socket module
import sys
import os
import datetime

host = socket.gethostname()     # Get local machine name
port=int(sys.argv[2])
file=sys.argv[1]
def request(file,port,host):
	print('stat',datetime.datetime.now())
	# s=None
	s = socket.socket()             # Create a socket object
	# port = 60001                    # Reserve a port for your service.
	# try:
	s.connect((host, port))
	# except socket.error:
	# print ('error')
	# return
	s.send("Hello server!"+host)

	with open(file, 'wb') as f:
	    print ('file opened')
	    while True:
	        # print('receiving data...')
	        data = s.recv(4096)
	#        print('data=%s', (data))
	        if not data:
	            break
	        # write data to a file
	        f.write(data)

	f.close()
	print('Successfully get the file')
	s.close()
	# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print('close','connection closed')
	print(datetime.datetime.now())
	return
request(sys.argv[1],int(sys.argv[2]),host)
