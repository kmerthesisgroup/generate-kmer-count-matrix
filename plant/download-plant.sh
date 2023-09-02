#!/bin/bash

curl "https://afproject.org/media/genome/std/assembled/plants/dataset/assembled-plants.zip" \
	--output plant.zip
mkdir -p data
unzip plant.zip
mv assembled-plants/* data
rm -rf assembled-plants

