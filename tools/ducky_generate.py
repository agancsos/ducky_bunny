#!/usr/bin/env python3
###############################################################################
# Name         : ducky_generate.py                                            #
# Author       : Abel Gancsos                                                 #
# Version      : v. 1.0.0.0                                                   #
# Description  : Helps generate a non-default static map.                     #
###############################################################################
import os, sys;

class DuckyGenerate:
	input_file=None;output_file=None;debug=None;
	def __init__(self, params=dict()):
		self.input_file = params["-i"] if "-i" in params.keys() else "";
		self.output_file = params["-o"] if "-o" in params.keys() else "";
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
	def invoke(self):
		assert self.input_file != "" and os.path.exists(self.input_file), "Input file cannot be empty and must exist...";
		assert self.output_file != "", "Output file cannot be empty...";
		result = "{";
		i = 0;
		with open(self.input_file, "r") as fh:
			line = fh.readline();
			while line != "":
				if self.debug: print(line);
				if "//" in line or line.strip() == "": line = fh.readline(); continue;
				comps = line.split(" = ");
				result += "{0}\"{1}\":\"{2}\"".format("," if i > 0 else "", comps[0].strip(), comps[1].strip());
				line = fh.readline();
				i += 1;
		result += "}";
		if self.debug: print(result);
		else:
			with open(self.output_file, "w") as fh: fh.write(result);
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = DuckyGenerate(params);
	session.invoke();

