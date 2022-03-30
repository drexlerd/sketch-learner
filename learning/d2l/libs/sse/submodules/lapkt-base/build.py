#!/usr/bin/python3

"""
    A helper build script - Builds the production library and vanilla solver
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import multiprocessing

def parse_arguments(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('--all', action='store_true', help="Flag to compile all modes.")
	parser.add_argument('--debug', action='store_true', help="Flag to compile in debug mode.")
	return parser.parse_args(args)

def single_build(directory, command):
	# Build the lapkt2 library
	print('\nBuilding "lapkt2 library"...')
	sys.stdout.flush()
	output = subprocess.call(command.split(), cwd=directory)
	if output:
		sys.exit(output)	

def get_command(cpus, debug):
	return 'scons -j {} {}'.format(cpus, debug)
	
def main(args):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	cpus = min(5, multiprocessing.cpu_count() - 1)
	print("Starting build process on directory '{}' with {} CPUs.".format(current_dir, cpus))
	
	if args.all:  # We launch a build for each possible debug config
		for debug_flag in ["edebug=1", "debug=1", ""]:
			single_build(current_dir, get_command(cpus, debug_flag))
		
	else:
		debug_flag = "debug=1" if args.debug else ""
		single_build(current_dir, get_command(cpus, debug_flag))

if __name__ == "__main__":
	main(parse_arguments(sys.argv[1:]))
