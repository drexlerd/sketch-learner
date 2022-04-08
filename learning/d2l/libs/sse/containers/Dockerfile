###############################################################################
# A first image to build the planner
###############################################################################
FROM ubuntu:20.04 AS builder

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/London"
ENV CXX g++

RUN apt-get update && apt-get install --no-install-recommends -y \
	build-essential \
	ca-certificates \
	cmake \
    curl \
	python3 \
    python3-pip \
	git \
	openssh-client \
	pkg-config \
	libboost-program-options-dev libboost-filesystem-dev libboost-system-dev \
	libboost-timer-dev libboost-serialization-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/

##### CLINGO INSTALLATION #####
## At the moment we simply download the 64-bit binaries and create and appropriate
## link to them which will be used afterwards as part of an environment variable
RUN curl -SL http://github.com/potassco/clingo/releases/download/v5.2.2/clingo-5.2.2-linux-x86_64.tar.gz | tar xz \
    && ln -s clingo-5.2.2-linux-x86_64 clingo

##### PLANNER INSTALLATION #####
# First build C++ code
ADD . planner
RUN cd planner \
    #&& git submodule update --init \
    && cmake -DCMAKE_BUILD_TYPE=Release -S . -B build \
    && cmake --build build -j4

RUN apt-get update && apt-get install --no-install-recommends -y python3-dev

# We install Python dependencies in a particular directory so that we can move them to the "runner" image more easily
# (see https://pythonspeed.com/articles/multi-stage-docker-python/)
RUN pip3 install --target=/workspace/pip -U -r planner/requirements.txt


###############################################################################
# The final image to run the planner
###############################################################################
FROM ubuntu:20.04 AS runner
MAINTAINER Guillem Francès guillem.frances@upf.edu

WORKDIR /workspace/

RUN apt-get update && apt-get install --no-install-recommends -y \
	python3 \
	libboost-program-options1.71.0 \
	libboost-filesystem1.71.0 \
	libboost-timer1.71.0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the elements necessary for execution from the previous docker build into this build:
# - Gringo binary:
COPY --from=builder /workspace/clingo/gringo /bin/
# - Planner binaries:
COPY --from=builder /workspace/planner/solver.bin /workspace/planner/
COPY --from=builder /workspace/planner/run.py /workspace/planner/
COPY --from=builder /workspace/planner/python /workspace/planner/python

# Copy all Python packages that were locally installed on the "builder" Docker image:
COPY --from=builder /workspace/pip /workspace/pip
# Update PYTHONPATH to include the pip-installed packages
ENV PYTHONPATH=/workspace/pip/:PYTHONPATH

## Set the appropriate library path for Gecode to be found:
ENV LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
# Make Clingo/Gringo available to the planner:
ENV GRINGO_PATH=/workspace/clingo


# ADD ./docker-entrypoint.sh /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]

ENTRYPOINT ["python3","/workspace/planner/run.py"]
