#!/usr/bin/env python3
# makes sure the script runs in Python3

"""
	File:		imu_csv.py
	Written by: 	Daniel Castle
	For: 		Dr. Kihei's research (secure traffic cabinets)

	Description:
		This Python script was created to track the orientation/motion of the Raspberry Pi
		SenseHat over time, with some context specific implementation for Dr. Kihei's research.

		The idea will be that the Pi will be attached to a door knob, with a person trying to perform
		an action on the door knob (either unlocking it normally, lockpicking it, or leaving it idle).
		The Pi will track the motion of the knob while the person does this, in order to use this data
		for a machine learning model created and run by Dr. Kihei. Hopefully, we can use the data to
		create a machine learning model that can reliably tell the difference between these actions.

	TODO:
		- A timer needs to be added that tracks the amount of time the script runs for. This time measurement
			also needs to be added to the csv writer so it gets written as part of the data.

		- The argv stuff in main for taking in command line arguments technically works, but it could be better.
			(replace with argparse library later, see StackAbuse article in doc/references.txt)

	References:
		Since this was my first time really doing a deep dive into Python, I had to use a lot of resources,
		to the point where it wouldn't be viable to put all the links to them in here. Instead, they are all
		linked in a file called "references.txt" in the doc folder of this repo. Check there for resources on
		how I made this script.

"""

# import statements
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

# key mode pattern for 8x8 RGB LED array
key_led_pattern = [
	black, black, black, black, black, black, black, black,				# first row
	black, black, black, black, black, yellow, yellow, black,			# second row
	black, black, black, black, yellow, black, black, yellow,			# third row
	yellow, yellow, yellow, yellow, yellow, black, black, yellow,			# fourth row
	yellow, black, yellow, black, yellow, black, black, yellow,			# fifth row
	yellow, black, yellow, black, black, yellow, yellow, black,			# sixth row
	black, black, black, black, black, black, black, black, 			# seventh row
	black, black, black, black, black, black, black, black				# eighth row
]

# no key mode pattern for 8x8 RGB LED array
nokey_led_pattern = [
	red, black, black, black, black, black, black, red,				# first row
	black, red, black, black, black, yellow, red, black,				# second row
	black, black, red, black, yellow, red, black, yellow,				# third row
	yellow, yellow, yellow, red, red, black, black, yellow,				# fourth row
	yellow, black, yellow, red, red, black, black, yellow,				# fifth row
	yellow, black, red, black, black, red, yellow, black,				# sixth row
	black, red, black, black, black, black, red, black, 				# seventh row
	red, black, black, black, black, black, black, red				# eighth row
]



def sigint_handler(signal_received, frame):

	# print exit message when SIGINT/ctrl-c interrupt is caught
	print("Exiting logger script")

	# clear the RGB LED array
	sense.clear()

	# exit Python
	exit(0)


def display_mode(mode):

	# switch statement to set current pattern for current mode
	current_pattern = {
		"pick"	:   pick_led_pattern,
		"key"	:   key_led_pattern,
		"nokey"	:   nokey_led_pattern
	}[mode]

	# set the current pattern on the 8x8 RGB LED array
	sense.set_pixels(current_pattern)


def pause_handler():
    
    # read new mode from user input
    new_mode = input("Logging script has been paused. Please input a new mode:")
    
    # return new mode
    return new_mode

def log_orientation(mode, name):

	# append start date and time of logging to file name/path
	# (this prevents file from being rewritten on next function call)
	file_path = "./log/" + name + "_" + "log" + "_" + datetime.now().strftime("%m_%d_%Y_%H_%M_%S") + ".csv"

	# import the csv library
	import csv

	# open the file at the specified path with write permission
	with open(file_path, 'w', newline='') as file:

		# create a list that defines the header for the csv
		csv_header = ['roll', 'pitch', 'yaw', 'datetime', 'mode', 'name']

		# create and instantiate a csv writer
		writer = csv.writer(file)

		# write the header to the csv file (once)
		writer.writerow(csv_header)

		while True:

			event = sense.stick.wait_for_event()
			
			if event.action = ACTION_PRESSED:
                            mode = pause_handler()
                            
			else:
                            # display the current mode on the 8x8 RGB LED array
                            display_mode(mode)

                            # create and instantiate orientation object and record orientation to it
                            orientation = sense.get_orientation_degrees()

                            # create data list variable and add orientation, current time, and mode
                            data = []
                            data.append( "%s" % orientation["roll"] ) # record roll
                            data.append( "%s" % orientation["pitch"] ) # record pitch
                            data.append( "%s" % orientation["yaw"] ) # record yaw
                            data.append(datetime.now().strftime("%m_%d_%Y_%H_%M_%S"))
                            data.append(mode)
                            data.append(name)

                            # write the data list to the csv file
                            writer.writerow(data)

                            # print the data list (for debug)
                            print("\n".join(map(str, data)))




# main function
if __name__ == "__main__":

	# create and instantiate sense-hat variable
	sense = SenseHat()

	#  create signal for SIGINT interrupt and handle it with sigint_handler function
	signal(SIGINT, sigint_handler)

	# check if the first argument is help
	if argv[1] == "-help" or argv[1] == "help" or argv[1] == "-h":
		print("		This script tracks the motion/orientation of the SenseHat, with different modes/types for tracking.")
		print("		Current working modes: key, nokey, pick")
		print(" 		Usage: python3 imu_csv.py [mode] [name]")
	# take in first and second argument as the mode and name respectively
	else:
		log_orientation(argv[1], argv[2])


