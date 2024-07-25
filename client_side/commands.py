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
	def __init__(self, client) -> None:
		from client import Client

		self.client:	Client = client

	def command(self, command_name: str, args: list) -> None:
		command_list = dir(self)
		
		if command_name in command_list:
			getattr(self, command_name)(args)

	def shell():
		pass

	def close(self, args: list) -> None:
		print("client closed")
		self.client.close()