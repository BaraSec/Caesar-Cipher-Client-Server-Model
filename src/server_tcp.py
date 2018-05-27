#!/usr/bin/python3


# importing required libraries
import socket, sys, threading


def Main():

	# Checking if not all arguments where given
	if(len(sys.argv) < 4):
		print("\n-------------------------------------\nUsage: " + sys.argv[0] + " IP PORT KEY\n-------------------------------------\n\n")
		exit()

	user_args = sys.argv[1:]

	# to catch non-numeric port values
	try:
		ip = str(user_args[0])
		port = int(user_args[1])
	except ValueError:
		print("\n\n--> Error: PORT must have numeric value!\n")
		exit()

	# to catch invalid KEY values
	if(int(user_args[2]) < 1 or int(user_args[2]) > 25):
		print("\n\n--> Error: KEY must be between 1 and 25 inclusively!\n")
		exit()

	# Creating a new TCP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# to find an available port starting from the given port
	while True:
		try:
			s.bind((ip, port))
			break
		except OSError:
			port += 1

	# Printing ip's and port's information
	print("\n\n---------------------\nIP: " + ip)
	print("---------------------\nPort: " + str(port) + "\n---------------------\n\n")

	key = int(user_args[2])

	# Starts listening for TCP connections
	s.listen(1)

	# To prevent server crash after client's disconnection
	while True:
		# Accepting a connection when found
		# and storing connected client's information
		# (socket object of the client, and the address it came from)
		client, address = s.accept()

		# Creating a new thread to serve the new client (this way it can serve many clients at the same time)
		t = threading.Thread(target=serve, args=(client, address, key))
		t.start()

# The encrypting method (function)
def caesarEncryptor(message, key):

	# Two helper mappings, from letters to integers and vice versa
	A2I = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
	I2A = dict(zip(range(26),"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

	encrypted = ""

	# To alter the original message letter by letter
	for letter in message:
		# If the letter is alphabetical
		if letter.isalpha(): 
			# if the letter is capital
			if letter.isupper():
				encrypted += I2A[(A2I[letter] + key) % 26]
			else:
				encrypted += I2A[(A2I[letter.upper()] + key) % 26].lower()
		else:
			encrypted += letter

	# Return the result
	return encrypted

def serve(client, address, key):
	# Printing connection information
	print("Connection from: " + str(address) + "\n")

	# To recieve all the sent messages from the client
	while True:
		# recieving messages from the client
		try:
			data = client.recv(1024).decode('utf-8')
		except ConnectionResetError:
			print("Disconnection from: " + str(address) + "\n")
			return

		# if the client closed the connection --> disconnect
		if not data:
			break

		# encrypting the message
		encrypted = caesarEncryptor(data, key)

		# sending the encrypted message to the client
		client.send(encrypted.encode('utf-8'))

	# Printing disconnection information
	print("Disconnection from: " + str(address) + "\n")

	# Closing the socket, and freeing the port
	client.close()

if __name__ == '__main__':
	try:
		Main()
	# if Ctrl+c was triggered
	except (KeyboardInterrupt, SystemExit):
		print("\n\n--> Server closed!\n")
		exit()
	except ConnectionResetError:
		print("\n\n--> A client was forcibly closed by the remote host!\n")