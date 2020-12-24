import socket                   # Import socket module
import sys
import os

# port = 60000                    # Reserve a port for your service.
# s = socket.socket()             # Create a socket object
# host = socket.gethostname()     # Get local machine name
# s.bind(("", port))            # Bind to the port
# s.listen(5)                     # Now wait for client connection.
q=["pics00","pics01","pics02"]

def send(p,file):					#p=port
	port=p
	filename=file
	# s=None
	s = socket.socket()             # Create a socket object
	# print ('Server listening....')
	try:
		s.bind(("", int(port)))
	except socket.error:
		print("error")
		return
	s.listen(5)
	# while len(q)!=0:
	conn, addr = s.accept()     # Establish connection with client. addr=req ip
	print ('Got connection from', addr)
	data = conn.recv(4096)
	# print('Server received', repr(data))

	# filename='abcd.txt'
	dir = filename[:-7]
	f = open( os.path.join( dir, filename ) ,"rb")
	l = f.read(4096)
	while (l):
	   conn.send(l)
	#   print('Sent ',repr(l))
	   l = f.read(4096)
	f.close()
	print('Done sending')
	conn.close()
	s.close()
	# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	return
send(sys.argv[1],sys.argv[2])
