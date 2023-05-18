#! /bin/bash

set -euo pipefail

# "release" or "debug"
BUILD_TYPE="$1"

# Get full directory name of the script (https://stackoverflow.com/a/246128).
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd ${SCRIPT_DIR}

cd ../../libs/dlplan

PREFIX="$(realpath .)"/installs/"$BUILD_TYPE"
BUILD_DIR="$(realpath .)"/builds/"$BUILD_TYPE"

cmake -DCMAKE_BUILD_TYPE=${BUILD_TYPE} -DCMAKE_INSTALL_PREFIX=${PREFIX} -S . -B ${BUILD_DIR}
cmake --build ${BUILD_DIR} -j$(nproc)
cmake --install ${BUILD_DIR}
