# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: TheRed <TheRed@students.42.fr>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/21 12:26:37 by TheRed            #+#    #+#              #
#    Updated: 2024/07/21 12:26:37 by TheRed           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
from threading import Thread

from client import Client
from commands import Command
from printer import Printer

class Server:
	def __init__(self) -> None:
		self.clients = []
		self.client_id = 0

		self.commands:	Command = Command(self)
		self.printer:	Printer = Printer(self)

		self.listen_thread = Thread(target=self.listen, args=())
		self.listen_thread.start()

		self.handleInput()

	def listen(self) -> None:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', 5454))

		s.listen(5)

		while True:
			client, addr = s.accept()
			
			new_client = Client(self, client, addr, len(self.clients))
			self.clients.append(new_client)

			Thread(target=self.handleClient, args=(new_client,)).start()

	def removeClient(self, client) -> None:
		self.clients.remove(client)
		for client in self.clients:
			client.client_id = self.clients.index(client)

	def handleClient(self, client) -> None:
		print(f"New client from {client.addr}")
		while True:
			data = client.recv()
			if not data:
				break

			print(f"Received data: {data}")

		client.close()

	def handleInput(self) -> None:
		while True:
			self.printer.prompt()
			
			args = input()
			args = args.split(' ')
			
			command = args[0]
			args = args[1:]

			self.commands.command(command, args)

	
