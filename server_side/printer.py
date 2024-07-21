# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    printer.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: TheRed <TheRed@students.42.fr>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/22 00:47:29 by TheRed            #+#    #+#              #
#    Updated: 2024/07/22 00:47:29 by TheRed           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import colorsys
from colorama import *

class Printer:
	def __init__(self, server) -> None:
		self.server = server

		init()

		self.banner()

	def hex_to_rgb(self, hex_color):
		hex_color = hex_color.lstrip('#')
		return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

	def lerp(self, start, end, t):
		return start + t * (end - start)
	
	def lerp_color(self, start_color, end_color, t):
		return tuple(int(self.lerp(s, e, t)) for s, e in zip(start_color, end_color))

	def rgb_to_ansi(self, r: int, g: int, b: int) -> int:
		return f"\033[38;2;{r};{g};{b}m"

	def generate_gradient(self, palette, n):
		num_colors = len(palette)
		colors = []
		for i in range(n):
			t = i / (n - 1) * (num_colors - 1)
			idx1 = int(t)
			idx2 = min(idx1 + 1, num_colors - 1)
			local_t = t - idx1
			colors.append(self.lerp_color(palette[idx1], palette[idx2], local_t))
		return colors

	def colorize_text(self, text, colors):
		colored_lines = [f"{self.rgb_to_ansi(*color)}{line}{Style.RESET_ALL}" for color, line in zip(colors, text)]
		return "\n".join(colored_lines)

	def banner(self) -> None:
		os.system('cls' if os.name == 'nt' else 'clear')

		palette = ["#6f2dbd", "#a663cc", "#499fff", "#b8d0eb", "#b9faf8"]
		banner_text = ["  ██████  ██▓ ███▄    █   ▄████  █    ██  ██▓     ▄▄▄       ██▀███   ██▓▄▄▄█████▓▓██   ██▓",
				 		"▒██    ▒ ▓██▒ ██ ▀█   █  ██▒ ▀█▒ ██  ▓██▒▓██▒    ▒████▄    ▓██ ▒ ██▒▓██▒▓  ██▒ ▓▒ ▒██  ██▒",
						"░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▒██░▒██░    ▒██  ▀█▄  ▓██ ░▄█ ▒▒██▒▒ ▓██░ ▒░  ▒██ ██░",
						"  ▒   ██▒░██░▓██▒  ▐▌██▒░▓█  ██▓▓▓█  ░██░▒██░    ░██▄▄▄▄██ ▒██▀▀█▄  ░██░░ ▓██▓ ░   ░ ▐██▓░",
						"▒██████▒▒░██░▒██░   ▓██░░▒▓███▀▒▒▒█████▓ ░██████▒ ▓█   ▓██▒░██▓ ▒██▒░██░  ▒██▒ ░   ░ ██▒▓░",
						"▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░▓    ▒ ░░      ██▒▒▒ ",
						"░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ░░▒░ ░ ░ ░ ░ ▒  ░  ▒   ▒▒ ░  ░▒ ░ ▒░ ▒ ░    ░     ▓██ ░▒░ ",
						"░  ░  ░   ▒ ░   ░   ░ ░ ░ ░   ░  ░░░ ░ ░   ░ ░     ░   ▒     ░░   ░  ▒ ░  ░       ▒ ▒ ░░  ",
						"      ░   ░           ░       ░    ░         ░  ░      ░  ░   ░      ░            ░ ░     ",
						"                                                                                  ░ ░     "]
		palette_rgb = [self.hex_to_rgb(color) for color in palette]
		colors = self.generate_gradient(palette_rgb, len(banner_text))
		colored_banner = self.colorize_text(banner_text, colors)
		print(colored_banner)
		print("\n\n")

	def prompt(self) -> None:
		client_name = "Singularity"
		client_id = self.server.client_id
		pwd = "~/"

		self.cyan(f"╭──(", end="")
		self.color(client_name, "#a663cc", end="")
		self.cyan(f")-", end="")
		self.color(f"[{client_id}]: ", "#db677a", end="")
		self.color(pwd, "#8777dd")
		self.cyan(f"╰─", end="")
		self.cyan("$ ", end="")

	def color(self, data: str, color: str, end="\n") -> None:
		print(self.rgb_to_ansi(*self.hex_to_rgb(color)) + data + Style.RESET_ALL, end=end)

	def red(self, data: str, end="\n") -> None:
		print(Fore.RED + data + Fore.RESET, end=end)
	def green(self, data: str, end="\n") -> None:
		print(Fore.GREEN + data + Fore.RESET, end=end)
	def yellow(self, data: str, end="\n") -> None:
		print(Fore.YELLOW + data + Fore.RESET, end=end)
	def blue(self, data: str, end="\n") -> None:
		print(Fore.BLUE + data + Fore.RESET, end=end)
	def magenta(self, data: str, end="\n") -> None:
		print(Fore.MAGENTA + data + Fore.RESET, end=end)
	def cyan(self, data: str, end="\n") -> None:
		print(Fore.CYAN + data + Fore.RESET, end=end)
	def white(self, data: str, end="\n") -> None:
		print(Fore.WHITE + data + Fore.RESET, end=end)
	def black(self, data: str, end="\n") -> None:
		print(Fore.BLACK + data + Fore.RESET, end=end)
	def lightblack(self, data: str, end="\n") -> None:
		print(Fore.LIGHTBLACK_EX + data + Fore.RESET, end=end)
	def lightred(self, data: str, end="\n") -> None:
		print(Fore.LIGHTRED_EX + data + Fore.RESET, end=end)
	def lightgreen(self, data: str, end="\n") -> None:
		print(Fore.LIGHTGREEN_EX + data + Fore.RESET, end=end)
	def lightyellow(self, data: str, end="\n") -> None:
		print(Fore.LIGHTYELLOW_EX + data + Fore.RESET, end=end)
	def lightblue(self, data: str, end="\n") -> None:
		print(Fore.LIGHTBLUE_EX + data + Fore.RESET, end=end)
	def lightmagenta(self, data: str, end="\n") -> None:
		print(Fore.LIGHTMAGENTA_EX + data + Fore.RESET, end=end)
	def lightcyan(self, data: str, end="\n") -> None:
		print(Fore.LIGHTCYAN_EX + data + Fore.RESET, end=end)
	def lightwhite(self, data: str, end="\n") -> None:
		print(Fore.LIGHTWHITE_EX + data + Fore.RESET, end=end)
	
	def reset(self) -> None:
		print(Fore.RESET)