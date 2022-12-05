import socket
from threading import Thread

class Client:
	def __init__(self,conn,addr):
		self.conn = conn
		self.addr = addr

	def send(self,text):
		self.conn.send(text.encode())

	def __repr__(self):
		return f"<Client addr:{self.addr[0]}:{self.addr[1]}>"

class Sock:
	def __init__(self,host,port,max_cons):
		# Values
		self.all_connections = []
		###

		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.bind((host,port))
		self.s.listen(max_cons)
		# Go into the loop
		self.loop()

	def loop(self):
		while True:
			conn,addr = self.s.accept()
			c = Client(conn,addr)
			t = Thread(target=self.connection,args=(c,))
			t.setDaemon(True)
			t.start()
		self.s.close()

	def broadcast(self,text,clist=None):
		if clist == None:
			clist = self.all_connections
		for c in clist:
			c.send(text)

	def connection(self,c):
		print(c,"has been connected.")
		self.connect(c)
		self.all_connections.append(c)
		while True:
			try:
				data = c.conn.recv(1024)
			except ConnectionResetError:
				break
			except ConnectionAbortedError:
				break
			except TimeoutError:
				break
			else:
				if data:
					data = data.decode()
					print(f"{c} send '{data}'.")
					self.receive(c,data)
				else:
					break
		c.conn.close()
		for index,i in enumerate(self.all_connections):
			if i.addr == c.addr:
				del self.all_connections[index]
		print(c,"has been cancelled.")
		self.disconnect(c)

	def connect(self,c):
		pass

	def receive(self,c,data):
		pass

	def disconncet(self,c):
		pass
