#!/bin/bash

curl "http://afproject.org/media/genome/std/assembled/plants/dataset/assembled-plants.zip" \
	--output plant.zip
unzip plant.zip
mv assembled-plant data

