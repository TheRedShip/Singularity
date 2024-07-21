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

class Command:
	def __init__(self, server) -> None:
		from server import Server

		self.server:	Server = server

	def command(self, command_name: str, args: list) -> None:
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

	def list(self, args: list) -> None:
		for client in self.server.clients:
			print(f"Client {client.client_id} from {client.addr}")