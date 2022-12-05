import socket
from tkinter import *
from tkinter.ttk import *
from threading import Thread

class Main:
	def __init__(self):
		self.server = ("127.0.0.1",25565)
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		Thread(target=self.ui,args=()).start()

	def send(self,text):
		self.s.send(text.encode())

	def ui(self):
		self.win = Tk()
		self.win.geometry("725x520")
		self.win.resizable(width=True, height=True)

		self.note = Notebook(self.win)
		self.note.pack(fill=BOTH,expand=True)

		self.chatframe = Frame(self.win,relief='ridge',borderwidth=1)
		self.note.add(self.chatframe,text="Chat")
		self.forumframe = Frame(self.win,relief='ridge',borderwidth=1)
		self.note.add(self.forumframe,text="Forum")

		self.message_show_text = Text(self.chatframe,width=100,height=34,relief=FLAT)
		self.message_show_text.grid(column=0,row=0)
		self.message_show_text_bar = Scrollbar(self.chatframe)
		self.message_show_text_bar.grid(column=1,row=0,sticky=N+S)
		self.enter_text = Text(self.chatframe,width=100,height=3)
		self.enter_text.grid(row=1,columnspan=2,sticky=N+S+W+E,ipady=0)
		self.message_show_text_bar.config(command=self.message_show_text.yview)
		self.message_show_text.config(yscrollcommand=self.message_show_text_bar.set)
		self.enter_text.bind("<Return>",self.send_input_text)
		self.enter_text.bind("<Control-Return>",self.nextline)

		t = Thread(target=self.listening,args=())
		t.setDaemon(True)
		t.start()

		self.win.mainloop()

	def send_input_text(self,event):
		data = self.enter_text.get(1.0,END).strip()
		self.enter_text.delete(1.0,END)
		self.send(data)
		return "break"

	def nextline(self,event):
		pass

	def code001(self,content):
		self.message_show_text.config(state=NORMAL)
		self.message_show_text.insert(END,content)
		self.message_show_text.config(state=DISABLED)
		self.message_show_text.see(END)

	def code002(self,content):
		self.message_show_text.config(state=NORMAL)
		self.message_show_text.delete(1.0,END)
		self.message_show_text.config(state=DISABLED)

	def listening(self):
		try:
			self.s.connect(self.server)
		# The server is not working
		# Report errors
		except ConnectionRefusedError:
			self.message_show_text.config(state=NORMAL)
			self.message_show_text.window_create(
				"insert",
				window=Label(self.message_show_text,
					text="Can't connect to the server.",
					font=("Arial",18,"bold")
				)
			)
			self.message_show_text.config(state=DISABLED)
		else:
			while True:
				d = self.s.recv(1024).decode()
				if d:
					type_ = d[0:3:1]
					content = d[3::1]
					if type_ == "001":
						self.code001(content)
					if type_ == "002":
						self.code002(content)
			self.s.close()

Main()
