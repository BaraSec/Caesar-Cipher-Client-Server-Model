#!/usr/bin/python3


# importing required libraries
import socket, sys


def Main():

	# Checking if not all arguments where given
	if(len(sys.argv) < 3):
		print("\n-------------------------------------\nUsage: " + sys.argv[0] + " IP PORT\n-------------------------------------\n\n")
		exit()

	user_args = sys.argv[1:]

	# to catch non-numeric port values
	try:
		host = str(user_args[0])
		port = int(user_args[1])
	except ValueError:
		print("\n\n--> Error: PORT must have numeric value!\n")
		exit()

	# Creating a new TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Catching different connection errors
	try:
		s.connect((host, port))
	except OSError:
		print("\n\n--> Connection error!")
		print("--> Usage: " + sys.argv[0] + " IP PORT\n\n")
		exit()

	# Accepting input (the message) from the user
	message = input("\nMessage (Ctrl+c to end) -> ")

	# Defining Ctrl+c as the closer bit
	while message != '^C':
		# skipping the "ENTER" presses
		while message == "":
			message = input("\nMessage (Ctrl+c to end) -> ")

		# Sending the message to the server as bytes
		s.send(message.encode('utf-8'))

		# Recieving the message as bytes and decoding it to a String
		data = s.recv(1024).decode('utf-8')

		# Printing the result
		print('---> Result from server: "' + data + '"')

		# Requesting a new message from the user
		message = input("\nMessage (Ctrl+c to end) -> ")

	# Closing the socket, and freeing the port
	s.close()

	

if __name__ == '__main__':
	try:
		Main()
	# if Ctrl+c was triggered
	except KeyboardInterrupt:
		print("\n\n--> Client closed!\n")
	# Catching different connection errors
	except ConnectionRefusedError:
		print("\n\n--> Connection refused!\n")
	except ConnectionResetError:
		print("\n\n--> Server went down!\n")
	except BrokenPipeError:
		print("\n\n--> Server went down or restarted.\nTry to Reconnect please!\n")