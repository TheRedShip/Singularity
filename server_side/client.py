# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    client.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: TheRed <TheRed@students.42.fr>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/21 12:49:59 by TheRed            #+#    #+#              #
#    Updated: 2024/07/21 12:49:59 by TheRed           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import json

class Client:
	def __init__(self, server, sock: socket.socket, addr: tuple, client_id: int) -> None:
		self.server = server

		self.client_id:	int				= client_id
		self.socket:	socket.socket	= sock
		self.addr:		tuple			= addr

		self.connected: bool 			= True

	def send(self, data: str, encoding=True) -> bool:
		try:
			if (encoding):
				data = data.encode()
			self.socket.sendall(data)
		except:
			return False
		return True

	def sendData(self, data_type: str, data: list) -> bool:
		payload = [data_type, data]
		return self.send(json.dumps(payload))

	def recv(self, size=1024, decoding="utf-8") -> str:
		try:
			response = self.socket.recv(size)
			return response.decode(decoding)
		except:
			return ""

	def close(self) -> None:
		if (not self.connected):
			return
		self.connected = False

		self.sendData("command", ["close", []])
		self.socket.close()
		self.server.removeClient(self)
		print(f"Connection from {self.addr} closed")