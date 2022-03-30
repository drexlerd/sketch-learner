#!/bin/bash
set -e

if [ "$1" = 'sse' ]; then
    # Pass only the relevant arguments to the main script
    exec /workspace/planner/run.py "${@:2}"
else
    exec "$@"
fi

