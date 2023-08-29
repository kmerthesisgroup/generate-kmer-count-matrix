#!/bin/bash

curl "https://afproject.org/media/genome/std/assembled/fish_mito/dataset/assembled-fish_mito.zip" \
	--output fish.zip
mkdir -p data
unzip fish.zip
mv assembled-fish_mito/* data
rm -rf assembled-fish_mito

