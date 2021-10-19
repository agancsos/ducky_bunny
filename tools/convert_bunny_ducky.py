#!/usr/bin/env python3
###############################################################################
# Name        : converty_bunny_ducky.py                                       #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Extracts a Ducky script from a Bunny script.                  #
###############################################################################
import os, sys;

class Convertor:
	source_path=None;target_path=None;
	ducky_lexicals = [
		"GUI",
		"ALT",
		"CTRL",
		"DELETE",
		"SHIFT",
		"MENU",
		"BREAK",
		"PAUSE",
		"HOME",
		"END",
		"ESC",
		"ESCAPE",
		"INSERT",
		"PAGEUP",
		"PAGEDOWN",
		"PRINTSCREEN",
		"SCROLLLOCK",
		"SPACE",
		" ",
		"TAB",
		"\t"	
	];
	def __init__(self, params=dict()):
		self.source_path = params["-s"] if "-s" in params.keys() else "";
		self.target_path = params["-t"] if "-t" in params.keys() else "";
	def invoke(self):
		assert self.source_path != "", "Source path cannot be empty...";
		ducky_script = "";
		with open(self.source_path, 'r') as fh:
			line = fh.readline();
			while (line != None and line != ""):
				if (line == "\n"): break;
				if (line[0] == "#"): line = "REM " + line;
				ducky_command = False;
				if (line.split(" ")[0] == "QUACK"): 
					ducky_command = True;
					line = line.replace("QUACK ", ""); 
				if (line.split(" ")[0] == "ATTACKMODE" or line.split(" ")[0] == "LED" or len(line.split("=")) > 1): 
					line = fh.readline();
					continue;
				if ducky_command and line.split(" ")[0] not in self.ducky_lexicals: continue;
				if (self.target_path == ""): print(line);
				else: ducky_script += line;
				line = fh.readline();
		if (self.target_path != ""):
			with open(self.target_path, 'w') as fh: fh.write(ducky_script);
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = Convertor(params);
	session.invoke();
	pass;
