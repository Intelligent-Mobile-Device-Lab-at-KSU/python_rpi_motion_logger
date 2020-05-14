"""
	File:		imu_csv.py
	Written by: 	Daniel Castle
	For: 		Dr. Kihei's research (secure traffic cabinets)

	References:
			https://pythonhosted.org/sense-hat/api/
			https://www.raspberrypi.org/documentation/hardware/sense-hat/
			https://projects.raspberrypi.org/en/projects/sense-hat-data-logger/
			https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat/
			https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python/
			https://simonwillison.net/2004/May/7/switch/
			https://stackoverflow.com/5445970/how-to-properly-print-a-list/
			https://devdungeon.com/content/python-catch-sigint-ctrl-c/
"""


from signal import signal, SIGINT
from sys import exit
from sense_hat import SenseHat
from csv import writer
from datetime import datetime

record_toggle = True
current_mode = "idle"


def sigint_handler(signal_received, frame):

	# print exit message when SIGINT/ctrl-c interrupt is caught
	print("Exiting logger script")
	exit(0)


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

	#  create signal for SIGINT interrupt and handle it with sigint_handler function
	signal(SIGINT, sigint_handler)

	# create and instantiate sense-hat variable
	sense = SenseHat()
	# log the orientation
	log_orientation(current_mode)
