#!/bin/bash

curl "https://afproject.org/media/genome/std/assembled/ecoli/dataset/assembled-ecoli.zip" \
	--output ecoli.zip
unzip ecoli.zip
mv assembled-ecoli data

