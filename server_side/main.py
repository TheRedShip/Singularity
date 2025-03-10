# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: TheRed <TheRed@students.42.fr>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/07/21 12:18:05 by TheRed            #+#    #+#              #
#    Updated: 2024/07/21 12:18:05 by TheRed           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import signal

from server import Server

serv = None

def signal_handler(sig, frame):
	global serv
	serv.close()

def main() -> None:
	global serv
	
	signal.signal(signal.SIGINT, signal_handler)

	serv = Server()
	serv.handleInput()

if __name__ == "__main__":
	main()
