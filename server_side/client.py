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
	def __init__(self, server, socket: socket.socket, addr: tuple, client_id: int) -> None:
		self.server = server

		self.client_id:	int				= client_id
		self.sock:		socket.socket	= socket
		self.addr:		tuple			= addr

		self.connected: bool 			= True

	def send(self, data: str) -> bool:
		try:
			self.sock.sendall(data.encode())
		except OSError:
			return False
		return True

	def sendData(self, data_type: str, data: list) -> bool:
		payload = [data_type, data]
		return self.send(json.dumps(payload))

	def recv(self) -> str:
		try:
			return self.sock.recv(1024).decode()
		except ConnectionResetError:
			return ""
		except ConnectionAbortedError:
			return ""

	def close(self) -> None:
		if (not self.connected):
			return
		self.connected = False

		self.sendData("command", ["close", []])
		self.sock.close()
		self.server.removeClient(self)
		print(f"Connection from {self.addr} closed")