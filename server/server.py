import re
from socket_builtins import Sock

class TempChat(Sock):
	'''
	Server-to-Client Data Format:
	`001msg` Chat Message
	`002` Clear The Chat Text
	...

	'''
	def __init__(self,host,port):
		self.onlines = []
		Sock.__init__(self,host,port,100)

	def online_names(self,function=lambda x:x):
		'''
		Do what to each element in onlines list
		'''
		return [function(i.name) for i in self.onlines]

	def receive(self,c,data):
		if hasattr(c,"name"):
			self.broadcast(f"001{c.name}:{data}\n")
		else:
			name = data.strip()
			match = re.findall(r"^[a-zA-Z_]{1,15}$",name)
			if match:
				name = match[0]
				if name.lower() not in self.online_names(lambda x:x.lower()):
					c.name = name
					self.broadcast(
						f"001* {name} joined\n",
						clist=self.onlines)
					self.onlines.append(c)
					c.send(f"002")
					c.send(f"001Onlines:{','.join(self.online_names())}\n")
					return 0
				else:
					c.send(f"001\nNickname taken\n")
			else:
				c.send(f"001\nToo long or too short!\n")
			c.send(f"001Enter your name by entry on the bottom:")
			return 0

	def connect(self,c):
		c.send(f"001Enter your name by entry on the bottom:")

	def disconnect(self,c):
		for i,cx in enumerate(self.onlines):
			if cx.addr == c.addr:
				del self.onlines[i]
				break
		if hasattr(c,"name"):
			self.broadcast(f"001* {c.name} left\n")

TempChat("0.0.0.0",25565)