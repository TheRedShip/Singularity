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

			self.printer.good(f"New client from {new_client.addr[0]} {new_client.addr[1]}")
			
			self.commands.persistance([], new_client)

	def getClient(self, client_id: int | None = None, error: bool = True) -> Client | bool:
		id = client_id
		if (client_id == None):
			id = self.client_id
		if (id < 0 or id >= len(self.clients)):
			if (error):
				self.printer.bad(f"Wrong client id\n")
			return False
		return self.clients[id]

	def removeClient(self, client: Client) -> None:
		self.clients.remove(client)
		for client in self.clients:
			client.client_id = self.clients.index(client)


	def handleInput(self) -> None:
		while True:
			self.printer.prompt()
			
			args = input()
			args = args.split(' ')
			
			command = args[0]
			args = args[1:]
			
			if (len(command) == 0):
				continue

			self.commands.command(command, args)

	def close(self) -> None:
		print("\n\n")
		self.printer.info("Catched exit..")
		
		for client in self.clients:
			client.close()
		self.socket.close()
		sys.exit(0)
	
