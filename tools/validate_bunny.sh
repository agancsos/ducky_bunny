#!/bin/bash
DISK_BASE_PATH="/Volumes/BashBunny"
FILES=(config.txt version.txt)
DIRS=(docs languages loot tools payloads payloads/extensions payloads/library payloads/switch1 payloads/switch2)
CREATE_MISSING=0
if [ "$1" != "" ]; then
	DISK_BASE_PATH="$1"
fi

for f in ${FILES[@]}; do
	printf "$DISK_BASE_PATH/$f\n"
	if [ ! -f "$DISK_BASE_PATH/$f" ]; then
		printf "File missing: %s\n" "$DISK_BASE_PATH/$f"
		if [ $CREATE_MISSING -eq 1 ]; then
			printf "Creating file: %s\n" "$DISK_BASE_PATH/$f"
			touch "$DISK_BASE_PATH/$f"
		fi
	fi
done

for  d in ${DIRS[@]}; do
	printf "$DISK_BASE_PATH/$d\n"
	if [ ! -d "$DISK_BASE_PATH/$d" ]; then
		printf "Directory missing: %s\n" "$DISK_BASE_PATH/$d"
		if [ $CREATE_MISSING -eq 1 ]; then
			printf "Creating directory %s\n" "$DISK_BASE_PATH/$d"
			mkdir "$DISK_BASE_PATH/$d"
		fi
	fi
done

