#!/usr/bin/python3

"""
    A helper installer
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import shutil
import fnmatch


def parse_arguments(args):
	parser = argparse.ArgumentParser(description="LAPKT module installer")
	parser.add_argument('--all', action='store_true', help="Flag to compile all modes.")
	parser.add_argument('--debug', action='store_true', help="Flag to compile in debug mode.")
	parser.add_argument('--dir', default=os.getenv('LAPKT', None), help="The directory where the module will be installed")
	return parser.parse_args(args)


def list_header_files(src_dir):
	#print(src_dir)
	return [os.path.join(dirpath, f)
					for dirpath, dirnames, files in os.walk(src_dir)
					for f in files if f.endswith('.hxx')]



def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s

def common_subpath_prefix(src, dst):
	prefix = os.path.commonprefix((src, dst))
	last_slash = prefix.rfind("/")
	return prefix[:last_slash+1]
	
def report_copied_file(src, dst):
	prefix = common_subpath_prefix(src, dst)
	print("{}  -->  {}".format(remove_prefix(src, prefix), remove_prefix(dst, prefix)))
	
def copy_headers(src_dir, dest_dir):
	print("Installing module files from dir '{}' to dir '{}'".format(src_dir, dest_dir))
	headers = list_header_files(src_dir)
	#print(headers)
	for header in headers:
		subpath = remove_prefix(header, src_dir + '/')
		dest_header = os.path.join(dest_dir, subpath)
		#print(subpath, dest_header)
		os.makedirs(os.path.dirname(dest_header), exist_ok=True)
		shutil.copy2(header, dest_header)
		
		report_copied_file(header, dest_header)
	

def copy_all(src_dir, dest_dir, ext):
	files = glob.iglob(os.path.join(src_dir, ext))
	for f in files:
		if os.path.isfile(f):
			shutil.copy2(f, dest_dir)
			report_copied_file(f, dest_dir)
			
			
def main(args):
	if args.dir is None:
		raise RuntimeError("You need to provide the directory where LAPKT will be installed")
	
	current_dir = os.path.dirname(os.path.abspath(__file__))
	
	src_dir = os.path.join(current_dir, 'src', 'lapkt')
	dest_dir = os.path.join(args.dir, 'include/lapkt')
	copy_headers(src_dir, dest_dir)
	
	src_dir = os.path.join(current_dir, 'lib')
	dest_dir = os.path.join(args.dir, 'lib/')
	os.makedirs(dest_dir, exist_ok=True)
	copy_all(src_dir, dest_dir, "*.so")

if __name__ == "__main__":
	main(parse_arguments(sys.argv[1:]))
