#!/bin/bash
###############################################################################
# Name        : helpers.sh                                                    #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Target      : ALL                                                           #
# Description : Custom Bash Bunny helpers.                                    #
###############################################################################

BASH_RUN() {
	local platform=$1
	local delay=$2
	local keyboard_delay=500
	shift 2

	case "$platform" in
		"WIN")
			QUACK GUI R
			QUACK DELAY $keyboard_delay
			QUACK STRING "$@"
			QUACK ENTER ;;
		"UNIX_SERVER")
			QUACK STRING "$@"
			QUACK ENTER
			QUACK DELAY $delay
			QUACK STRING "history -c"
			QUACK ENTER ;;
		"UNIX_DESKTOP")
			QUACK ALT F2
			QUACK DELAY $keyboard_delay
			QUACK STRING "$@"
			QUACK ENTER
			QUACK DELAY $delay
			QUACK STRING "history -c" ;;		
		"MAC")
			QUACK GUI SPACE
			QUACK STRING terminal
			QUACK DELAY $keyboard_delay
			QUACK ENTER
			QUACK STRING "$@"
			QUACK ENTER
			QUACK DELAY $delay
			QUACK STRING "history -c"
			QUACK ENTER ;;
		*) ;;
	esac
}

BUNNY_RUN() {
	BASH_RUN "$@"
}

BUNNY_LOG() {
	local log_path=$1
	shift
	echo "$(date) $@" >> "$log_path"
}

BUNNY_GET() {
	local var=$1
	local target=$2
	shift 2
	case "$var" in 
		"TARGET_OS") 
			raw_os=`nmap -T4 -O "$target" -sS | grep -i running:`
			if [[ "$raw_os" == *"Apple"* ]]; then
    			export "$var"= "mac"
			elif [[ "$raw_os" == *"Linux"* ]]; then
    			export "$var"="linux"
			elif [[ "$raw_os" == *"Microsoft"* ]]; then
				export "$var"="win"
			else
				export "$var"="NA"
			fi ;;
		*) ;;
	esac
}


export -f BUNNY_LOG
export -f BASH_RUN
export -f BUNNY_RUN
export -f BUNNY_GET

