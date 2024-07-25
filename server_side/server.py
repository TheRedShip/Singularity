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

import sys
import socket
from threading import Thread

from client import Client
from commands import Command
from printer import Printer


class Server:
	def __init__(self) -> None:
		self.clients:	list[Client]	= []
		self.client_id:	int				= 0

		self.commands:	Command = Command(self)
		self.printer:	Printer = Printer(self)

		self.socket:	socket.socket = None

		self.listen_thread = Thread(target=self.listen, args=())
		self.listen_thread.start()


	def listen(self) -> None:
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('', 5454))

		self.socket.listen(5)

		while True:
			try:
				client, addr = self.socket.accept()
			except OSError:
				break

			new_client = Client(self, client, addr, len(self.clients))
			self.clients.append(new_client)

			Thread(target=self.handleClient, args=(new_client,)).start()

	def removeClient(self, client: Client) -> None:
		self.clients.remove(client)
		for client in self.clients:
			client.client_id = self.clients.index(client)

	def handleClient(self, client: Client) -> None:
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


	def close(self) -> None:
		print("\n\nExiting...")
		
		for client in self.clients:
			client.close()

		self.socket.close()

		sys.exit(0)
	
