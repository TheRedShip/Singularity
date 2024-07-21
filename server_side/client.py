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

class Client:
	def __init__(self, server, socket: socket.socket, addr: tuple, client_id: int) -> None:
		self.server = server

		self.client_id:	int				= client_id
		self.sock:		socket.socket	= socket
		self.addr:		tuple			= addr

	def send(self, data: str) -> None:
		self.sock.sendall(data.encode())
	
	def recv(self) -> str:
		try:
			return self.sock.recv(1024).decode()
		except ConnectionResetError:
			return ""

	def close(self) -> None:
		self.sock.close()
		self.server.removeClient(self)
		print(f"Connection from {self.addr} closed")