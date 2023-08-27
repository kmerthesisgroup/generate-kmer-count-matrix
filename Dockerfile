FROM python:3.10.12-bookworm
RUN apt update && \
	apt install -y flex bison jellyfish g++ curl unzip time 
COPY ./ /workspace
WORKDIR /workspace
RUN cd merge && ./build.sh && cd .. && \
	cd parse-newick && ./build.sh 
