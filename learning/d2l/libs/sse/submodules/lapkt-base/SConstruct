
import os
import fnmatch
import itertools

HOME = os.path.expanduser("~")

# read variables from the cache, a user's custom.py file or command line arguments
vars = Variables(['variables.cache', 'custom.py'], ARGUMENTS)
vars.Add(BoolVariable('debug', 'Debug build', 'no'))
vars.Add(BoolVariable('edebug', 'Extreme debug', 'no'))

def which(program):
	""" Helper function emulating unix 'which' command """
	for path in os.environ["PATH"].split(os.pathsep):
		path = path.strip('"')
		exe_file = os.path.join(path, program)
		if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
			return exe_file
	return None

def locate_source_files(base_dir, pattern):
	matches = []
	for root, dirnames, filenames in os.walk(base_dir):
		for filename in fnmatch.filter(filenames, pattern):
			matches.append(os.path.join(root, filename))
	return matches

# Use clang unless gcc=c++ is specified
gcc = 'clang' if which('clang') and ARGUMENTS.get('gcc', 'clang') != 'g++' else 'g++'
env = Environment(variables=vars, ENV=os.environ, CXX=gcc)

# Determine the build directory name
if env['edebug']:
	build_dirname = '_build/edebug'
elif env['debug']:
	build_dirname = '_build/debug'
else:
	build_dirname = '_build/prod'
env.VariantDir(build_dirname, '.')

Help(vars.GenerateHelpText(env))

env.Append(CCFLAGS = ['-Wall', '-pedantic', '-std=c++11' ])  # Flags common to all options
if gcc == 'clang': # Get rid of annoying warning message from the Jenkins library
	env.Append(CCFLAGS = ['-Wno-deprecated-register' ])

# Extreme debug implies normal debug as well
if env['debug'] or env['edebug']:
	env.Append(CCFLAGS = ['-g', '-DDEBUG' ])
	lib_name = 'lapkt-debug'
else:
	env.Append(CCFLAGS = ['-O3', '-DNDEBUG' ])
	lib_name = 'lapkt'

# Additionally, extreme debug implies a different name plus extra compilation flags
if env['edebug']:
	env.Append(CCFLAGS = ['-DEDEBUG'])
	lib_name = 'lapkt-edebug'


# Base include directories
include_paths = ['src']
isystem_paths = [HOME + '/local/include']

sources = locate_source_files('src', '*.cxx')

env.Append( CPPPATH = [ os.path.abspath(p) for p in include_paths ] )
env.Append( CCFLAGS = [ '-isystem' + os.path.abspath(p) for p in isystem_paths ] )

build_files = [build_dirname + '/' + src for src in sources]

shared_lib = env.SharedLibrary('lib/' + lib_name, build_files)
static_lib = env.Library('lib/' + lib_name, build_files)

Default([static_lib, shared_lib])
