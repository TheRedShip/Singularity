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

import socket
from time import sleep

class Client:
	def __init__(self) -> None:
		self.s = None

		self.initSocket()

	def connectSocket(self) -> None:
		try:
			print("trying..")

			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect(('localhost', 5454))
		
		except ConnectionRefusedError:
			sleep(5)
			self.connectSocket()

	def initSocket(self) -> None:
		self.connectSocket()

		while True:
			data = self.recv()
			if not data:
				break
			print(f"Received data: {data.decode()}")
		
		self.initSocket()

	def recv(self) -> str:
		try:
			return self.s.recv(1024).decode()
		except ConnectionResetError:
			return ""