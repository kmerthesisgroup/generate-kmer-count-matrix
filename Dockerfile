FROM python:3.10.12-bookworm
RUN apt update && \
	apt install -y flex bison jellyfish g++ python3 curl unzip 
COPY ./ /workspace
WORKDIR /workspace
