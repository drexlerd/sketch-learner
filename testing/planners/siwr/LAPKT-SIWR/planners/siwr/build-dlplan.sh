#! /bin/bash

set -euo pipefail

# "release" or "debug"
BUILD_TYPE="$1"

# Get full directory name of the script (https://stackoverflow.com/a/246128).
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd ${SCRIPT_DIR}

cd ../../libs/dlplan

PREFIX="$(realpath .)"/installs/"$BUILD_TYPE/dlplan/"
BUILD_DIR="$(realpath .)"/builds/"$BUILD_TYPE"

echo $SCRIPT_DIR
echo $PREFIX 
echo $BUILD_DIR

cmake -DCMAKE_BUILD_TYPE=${BUILD_TYPE} -S . -B ${BUILD_DIR}
cmake --build ${BUILD_DIR} -j$(nproc)
cmake --install ${BUILD_DIR} --prefix=${PREFIX}
