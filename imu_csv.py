"""
	File:		imu_csv.py
	Written by: 	Daniel Castle
	For: 		Dr. Kihei's research (secure traffic cabinets)
"""


from signal import signal, SIGINT
from sys import exit
from sense_hat import SenseHat
from csv import writer
from datetime import datetime
from sys import argv

# color definitions for SenseHat 8x8 RGB LED array
red	 = (255,0,0)
green	 = (0,255,0)
blue	 = (0,0,255)
cyan	 = (0,255,255)
pink	 = (255,0,255)
yellow	 = (255,255,0)
black	 = (0,0,0)

# lock pick mode pattern for 8x8 RGB LED array
pick_led_pattern = [
	black, blue, black, black, cyan, cyan, cyan, black,				# first row
	blue, black, blue, black, black, cyan, black, black,				# second row
	blue, blue, black, black, black, cyan, black, black,				# third row
	blue, black, black, black, cyan, cyan, cyan, black,				# fourth row
	black, pink, pink, black, yellow, black, black, black,				# fifth row
	pink, black, black, black, yellow, black, yellow, black,			# sixth row
	pink, black, black, black, yellow, yellow, black, black,			# seventh row
	black, pink, pink, black, yellow, black, yellow, black				# eighth row
]

# idle mode pattern for 8x8 RGB LED array
idle_led_pattern = [
	blue, blue, blue, black, cyan, cyan, black, black,				# first row
	black, blue, black, black, cyan, black, cyan, black,				# second row
	black, blue, black, black, cyan, black, cyan, black,				# third row
	blue, blue, blue, black, cyan, cyan, black, black,				# fourth row
	pink, black, black, black, yellow, yellow, yellow, black,			# fifth row
	pink, black, black, black, yellow, black, black, black,				# sixth row
	pink, black, black, black, yellow, yellow, black, black,			# seventh row
	pink, pink, pink, black, yellow, yellow, yellow, black				# eighth row
]

# lock mode pattern for 8x8 RGB LED array
lock_led_pattern = [
	blue, black, black, black, black, cyan, black, black,				# first row
	blue, black, black, black, cyan, black, cyan, black,				# second row
	blue, black, black, black, cyan, black, cyan, black,				# third row
	blue, blue, blue, black, black, cyan, black, black,				# fourth row
	black, pink, pink, black, yellow, black, black, black,				# fifth row
	pink, black, black, black, yellow, black, yellow, black,			# sixth row
	pink, black, black, black, yellow, yellow, black, black, 			# seventh row
	black, pink, pink, black, yellow, black, yellow, black				# eighth row
]

# unlock mode pattern for 8x8 RGB LED array
unlock_led_pattern = [
	blue, black, blue, cyan, black, black, cyan, black,				# first row
	blue, black, blue, cyan, cyan, black, cyan, black,				# second row
	blue, black, blue, cyan, black, cyan, cyan, black,				# third row
	blue, blue, blue, cyan, black, black, cyan, black,				# fourth row
	pink, black, black, black, yellow, black, black, black,				# fifth row
	pink, black, black, black, yellow, black, yellow, black,			# sixth row
	pink, black, black, black, yellow, yellow, black, black,			# seventh row
	pink, pink, pink, black, yellow, black, yellow, black				# eighth row
]


def sigint_handler(signal_received, frame):

	# print exit message when SIGINT/ctrl-c interrupt is caught
	print("Exiting logger script")
	sense.clear()
	exit(0)


def display_mode(mode):

	# switch statement to set current pattern for current mode
	current_pattern = {
		"unlock": unlock_led_pattern,
		"lock"	:   lock_led_pattern,
		"pick"	:   pick_led_pattern,
		"idle"	:   idle_led_pattern
	}[mode]

	# set the current pattern on the 8x8 RGB LED array
	sense.set_pixels(current_pattern)


def log_orientation(mode):

	# append start date and time of logging to file name/path
	# (this prevents file from being rewritten on next function call)
	file_path = "./log/" + mode + "/" + mode + "_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".csv"

	# import the csv library
	import csv

	# open the file at the specified path with write permission
	with open(file_path, 'w', newline='') as file:

		# create a list that defines the header for the csv
		csv_header = ['orientation', 'datetime', 'mode']


		# create and instantiate a csv writer
		writer = csv.writer(file)

		# write the header to the csv file (once)
		writer.writerow(csv_header)

		while True:
			#  create signal for SIGINT interrupt and handle it with sigint_handler function
			signal(SIGINT, sigint_handler)

			# display the current mode on the 8x8 RGB LED array
			display_mode(mode)

			# create data list variable and add orientation, current time, and mode
			data = []
			data.append(sense.get_orientation_degrees())
			data.append(datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))
			data.append(mode)

			# write the data list to the csv file
			writer.writerow(data)

			# print the data list (for debug)
			print("\n".join(map(str, data)))


# main function
if __name__ == "__main__":

	# create and instantiate sense-hat variable
	sense = SenseHat()

	# check if the first argument is help
	if argv[1] == "-help" or argv[1] == "help" or argv[1] == "-h":
		print("		This script tracks the motion/orientation of the SenseHat, with different modes for tracking.")
		print("		Current working modes: lock, unlock, idle, pick")
	# take in first argument as the mode
	else:
		log_orientation(argv[1])

