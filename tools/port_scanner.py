#!/usr/bin/env python3
###############################################################################
# Name        : port_scanner.py                                               #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Scans the ports of a target IP address.                       #
###############################################################################
import os, sys, socket, threading;

class Scanner:
	target_ip=None;wait=None;
	def __init__(self, params=dict()):
		self.target_ip = params["-t"] if "-t" in params.keys() else "172.16.64.10";
		self.wait = params["-w"] if "-w" in params.keys() else "1";
	def check(self, port):
		rsp = os.system("ping -c 1 -W {0} {1}i{2} > /dev/null 2>&1".format(self.wait, self.target_ip, port));
		if (rsp == 0): print("{0}:{1}".format(self.target_ip, port));
	def invoke(self):
		for i in range(0, 7000): 
			t = threading.Thread(target=self.check, args=("{0}".format(i),));
			t.start();
			t.join();
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = Scanner(params);
	session.invoke();
	pass;

