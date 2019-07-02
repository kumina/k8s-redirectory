# Build stage
# -----------
FROM registry.kumina.nl/kumina/debian-python:3.7 as hyperscan_builder

# Set a few vars to help later on
ENV WORKDIR=/hyperscan
ENV HS_SOURCE=$WORKDIR/source
ENV HS_FINAL_BUILD=$WORKDIR/build
ENV HS_GIT="https://github.com/intel/hyperscan.git"
ENV HS_VERSION="v5.1.1"

# Update packages and install needed dependacies for build hyperscan
RUN apt-get update && \
    apt-get install -y cmake ragel libboost-all-dev git build-essential

# Set workdir and clone the source from official hyperscan git repo
WORKDIR $WORKDIR
RUN git clone $HS_GIT $HS_SOURCE --branch=$HS_VERSION

# Build and install hyperscan as a static library
RUN cd $HS_SOURCE && \
    mkdir build && \
    cd build && \ 
    cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -G "Unix Makefiles" ../ && \
    make -j6 && \
    make install

# Gather all needed files after installation into final build folder
RUN mkdir $HS_FINAL_BUILD && \
    cp /usr/include/hs/hs.h $HS_FINAL_BUILD && \
    cp /usr/include/hs/hs_common.h $HS_FINAL_BUILD && \
    cp /usr/include/hs/hs_compile.h $HS_FINAL_BUILD && \
    cp /usr/include/hs/hs_runtime.h $HS_FINAL_BUILD && \
    cp /usr/lib/x86_64-linux-gnu/pkgconfig/libhs.pc $HS_FINAL_BUILD && \
    cp /usr/lib/x86_64-linux-gnu/libhs_runtime.a $HS_FINAL_BUILD && \
    cp /usr/lib/x86_64-linux-gnu/libhs.a $HS_FINAL_BUILD

# Strip binaries to minimize space
RUN strip -d $HS_FINAL_BUILD/libhs.a && \
    strip -d $HS_FINAL_BUILD/libhs_runtime.a

# Real stage
# ----------
FROM registry.kumina.nl/kumina/debian-python:3.7

# Set a few vars to help later on
ENV HS_FINAL_BUILD=/hyperscan/build
ENV HS_FILE_DEST_H=/usr/include/hs
ENV HS_FILE_DEST_A=/usr/lib/x86_64-linux-gnu/
ENV HS_FILE_DEST_PC=/usr/lib/x86_64-linux-gnu/pkgconfig/

# Create needed directories
RUN mkdir -p $HS_FINAL_BUILD && \
    mkdir -p $HS_FILE_DEST_H && \
    mkdir -p $HS_FILE_DEST_A && \
    mkdir -p $HS_FILE_DEST_PC

# Copy files from previous stage
COPY --from=hyperscan_builder $HS_FINAL_BUILD $HS_FINAL_BUILD

# Put files in correct places
RUN mv $HS_FINAL_BUILD/*.h $HS_FILE_DEST_H && \
    mv $HS_FINAL_BUILD/*.a $HS_FILE_DEST_A && \
    mv $HS_FINAL_BUILD/*.pc $HS_FILE_DEST_PC

# Clean up after moving files in correct places
RUN rm -rf $HS_FINAL_BUILD
