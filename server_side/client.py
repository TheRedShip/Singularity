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
import struct
import json

class Client:
	def __init__(self, server, sock: socket.socket, addr: tuple, client_id: int) -> None:
		self.server = server

		self.client_id:	int				= client_id
		self.socket:	socket.socket	= sock
		self.addr:		tuple			= addr

		self.connected: bool 			= True
		
		self.path:	str				= "~"

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

	def recvLength(self, bytes: int) -> bytearray | None:
		data = bytearray()
		while len(data) < bytes:
			packet = self.socket.recv(bytes - len(data))
			if not packet:
				return None
			data.extend(packet)
		return data

	def recv(self, decoding="utf-8") -> str | bool:
		try:
			raw_length = self.recvLength(4)
			if not raw_length:
				return None
			length = struct.unpack('>I', raw_length)[0]
			return self.recvLength(length).decode(decoding)
		except:
			self.close()
			return False

	def close(self) -> None:
		if (not self.connected):
			return
		self.connected = False

		self.sendData("command", ["close", []])
		self.socket.close()
		self.server.removeClient(self)
		self.server.printer.bad(f"{self.client_id} : {self.addr} disconnected\n")