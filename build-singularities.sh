#!/bin/bash

# build planners
cd testing/planners/
cd siw && singularity build ../siw.img siw.sif && cd ..
cd siwr && singularity build ../siwr.img siwr.sif && cd ..
cd bfws && singularity build ../dual-bfws.img dual-bfws.sif && cd ..
cd lama && singularity build ../lama-first.img lama-first.sif && cd ..
cd ../../

# build sse
cd learning/d2l/libs/sse
docker build -t sse -f containers/Dockerfile .
singularity build sse.sif docker-daemon://sse:latest
cd ../../../../