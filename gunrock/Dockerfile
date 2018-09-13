FROM nvidia/cuda:9.2-devel-ubuntu18.04

WORKDIR /

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake git libboost-all-dev && rm -rf /var/lib/apt/lists/*

RUN git clone --recursive https://github.com/gunrock/gunrock.git && \
    cd gunrock && mkdir build && cd build && cmake .. && make -j$(nproc)

RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install pipenv numpy scipy
