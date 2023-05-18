#!/usr/bin/python3
import os
import sys
import subprocess

from pathlib import Path

LWAPTK_ROOT = Path('../..').resolve()

def main() :

    # 1. Install DLPlan
    config_name = 'release'
    assert config_name == 'release'
    subprocess.check_call(['./build-dlplan.sh', config_name], cwd=Path('.'))

	# 2. Call scons to build
    if len(sys.argv) > 1:
            rv = os.system( "scons %s" % sys.argv[1] )
    else:
        rv = os.system( 'scons -j 8' )

    if rv != 0 :
        sys.stderr.write("Build failed!")
        sys.exit(1)


if __name__ == '__main__' :
	main()
