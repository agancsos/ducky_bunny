#!/bin/bash
###############################################################################
# Name        : sync_gits.sh                                                  #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps sync Git repositories.                                  #
###############################################################################
BASE_PATH=$(dirname $0)
ROOT_PATH=$(dirname $0)/../../..
KEEP_FILES=0
JAR_VALUE=
PYTHON_VALUE=
GO_VALUE=

while getopts "p:k:" option; do
    case $option in
        p) BASE_PATH=$OPTARG ;;
		k) KEEP_FILES=$OPTARG ;;
        *) ;;
    esac
done

JAR_VALUE=$(java -jar $ROOT_PATH/tools/duckencoder.jar -i $BASE_PATH/payload.txt -o $BASE_PATH/inject_jar.bin > /dev/null; hexdump $BASE_PATH/inject_jar.bin)
PYTHON_VALUE=$(python3 $ROOT_PATH/tools/duckencoder.py -i $BASE_PATH/payload.txt -o $BASE_PATH/inject_py.bin > /dev/null; hexdump $BASE_PATH/inject_py.bin)
GO_VALUE=$(go run $ROOT_PATH/tools/duckyencoder.go -l $ROOT_PATH/tools/duckencoder_maps.json -i $BASE_PATH/payload.txt -o $BASE_PATH/inject_go.bin > /dev/null; hexdump $BASE_PATH/inject_go.bin)

echo "JAR    : $JAR_VALUE"
echo "PYTHON : $PYTHON_VALUE"
echo "GO     : $GO_VALUE"

if [ "$JAR_VALUE" = "$PYTHON_VALUE" ] && [ "$GO_VALUE" = "$PYTHON_VALUE" ]; then
	echo "Same!"
else
	echo "Not the same..."
fi

if [ $KEEP_FILES -lt 1 ]; then
	rm $BASE_PATH/inject_*.bin
fi

