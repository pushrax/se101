import socket

HOST = '127.0.0.1' # Symbolic name meaning the local host
PORT = 5005 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print 'Connected by', addr

while 1:
	data = conn.recv(1024)
	if not data:
		break
	print data
	#conn.send(data)
	conn.send('pos 1000 1000 0\n')
	conn.send('block 10 6\n')
	conn.send('path 3 3 3 4 3 5 4 5\n')

conn.close()
