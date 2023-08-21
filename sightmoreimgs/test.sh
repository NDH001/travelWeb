#!/bin/bash
#to scrap images
INPUT=sight_imgs_all.csv
OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found "; exit 99;}

while read id name img img_local fk
do
	echo $id
	curl -O $img
done < $INPUT
IFS=$OLDIFS
