#!/bin/bash
###############################################################################
# Name        : sync_gits.sh                                                  #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps sync Git repositories.                                  #
###############################################################################
BASE_PATH=$(dirname $0)/../
INPUT_PATH=payload.txt
JAR_MODE=0
while getopts "i:r:e:j:" option; do
    case $option in
        i) INPUT_PATH=$OPTARG ;;
		r) BASE_PATH=$OPTARG ;;
		j) JAR_MODE=$OPTARG ;;
        *) ;;
    esac
done

if [ $JAR_MODE = 0 ]; then
<<<<<<< HEAD
	go run $BASE_PATH/tools/duckyencoder.go -l $BASE_PATH/duckencoder_maps.json -i $BASE_PATH/payloads/payload.txt -o $BASE_PATH/inject.bin
=======
	go run $BASE_PATH/tools/duckyencoder.go  -i $BASE_PATH/payloads/payload.txt -o $BASE_PATH/inject.bin
>>>>>>> ad4a8fc9cef5de3ae77d36d605bd1e6f078f11b9
elif [ $JAR_MODE = 2 ]; then
	python3 $BASE_PATH/tools/duckencoder.py  -i $BASE_PATH/payloads/payload.txt -o $BASE_PATH/inject.bin
else
	java -jar $BASE_PATH/tools/duckencoder.jar -i $BASE_PATH/payloads/payload.txt -o $BASE_PATH/inject.bin
fi

