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
	shift
	local delay=$2
	local keyboard_delay=500
	shift

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

BUNNY_LOG() {
	local log_path=$1
	shift
	echo "$(date) $@" >> "$log_path"
}

export -f BUNNY_LOG
export -f BASH_RUN
