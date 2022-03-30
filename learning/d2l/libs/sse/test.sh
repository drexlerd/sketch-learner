#!/bin/bash
#set -e

# Simply use a few instances that we know will end fast
declare -a instances=("$DOWNWARD_BENCHMARKS/organic-synthesis-opt18-strips/p01.pddl"
  "$DOWNWARD_BENCHMARKS/scanalyzer-opt11-strips/p01.pddl"
  "$DOWNWARD_BENCHMARKS/blocks/probBLOCKS-4-0.pddl"
  "$DOWNWARD_BENCHMARKS/gripper/prob01.pddl"
  "$DOWNWARD_BENCHMARKS/mystery/prob01.pddl"
  "$DOWNWARD_BENCHMARKS/pathways/p01.pddl"
)


for i in "${instances[@]}"
do
  ./run.py --driver sse -i "$i"
  exitcode=$?
  if [ $exitcode -ne 11 ]; then
      exit $exitcode
  fi
done

echo "DONE!"