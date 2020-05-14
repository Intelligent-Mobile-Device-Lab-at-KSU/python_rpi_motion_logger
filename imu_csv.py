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

record_toggle = True
current_mode = "idle"

# color definitions for SenseHat 8x8 RGB LED array
red	 = (255,0,0)
green	 = (0,255,0)
blue	 = (0,0,255)
cyan	 = (0,255,255)
pink	 = (255,0,255)
yellow	 = (255,255,0)
black	 = (0,0,0)


def record_color(record_toggle):

	# if recording, make the LED color red (like a camcorder)
	if record_toggle == True:
		return red
	# make the LED color green if not recording
	else:
		return green


# lock pick mode pattern for 8x8 RGB LED array
pick_led_pattern = [
	black, blue, black, black, cyan, cyan, cyan, record_color(record_toggle),	# first row
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
	blue, blue, blue, black, cyan, cyan, black, record_color(record_toggle),	# first row
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
	blue, black, black, black, black, cyan, black, record_color(record_toggle),	# first row
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
	blue, black, blue, cyan, black, black, cyan, record_color(record_toggle),	# first row
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
	exit(0)

def dislay_mode(mode):
	return 0

def log_orientation(mode):


	# switch statement to set file path using mode parameter
	"""
	file_path = {
		"unlock": "imu_unlock",
		"lock"	: "imu_lock",
		"pick"	: "imu_pick",
		"idle"	: "imu_idle"
	}[mode]
	"""
	# append start date and time of logging to file name/path
	# (this prevents file from being rewritten on next function call)
	file_path = "./log/" + mode + "/" + mode + "_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".csv"

	# open the file at the specified path with write permission
	with open(file_path, 'w', newline='') as file:

		import csv
		# create and instantiate a csv writer
		writer = csv.writer(file)
		while True:

			#  create signal for SIGINT interrupt and handle it with sigint_handler function
			signal(SIGINT, sigint_handler)

			# create data list variable and add orientation, current time, and mode
			data = []
			data.append(sense.get_orientation_degrees())
			data.append(datetime.now())
			data.append(mode)

			# write the data list to the csv file
			writer.writerow(data)

			# print the data list (for debug)
			print("\n".join(map(str, data)))

			# break out of the logging loop if recording is turned off
			if record_toggle == False:
				break






# main function
if __name__ == "__main__":


	# create and instantiate sense-hat variable
	sense = SenseHat()

	sense.set_pixels(unlock_led_pattern)

	# log the orientation
	log_orientation(current_mode)
