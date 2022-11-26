#!/bin/bash

curl "http://afproject.org/media/genome/std/assembled/fish_mito/dataset/assembled-fish_mito.zip" \
	--output fish.zip
unzip fish.zip
mv assembled-fish_mito data

