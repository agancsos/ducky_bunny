#!/usr/bin/env python3
###############################################################################
# Name         : duckencoder.py                                               #
# Author       : Abel Gancsos                                                 #
# Version      : v. 1.0.0.0                                                   #
# Description  : Encodes a bin file for use with a USB Rubber Ducky.          #
###############################################################################
import os, sys, json;

class DuckyEncoder:
	keyboard_file=None;input_file=None;output_file=None;debug=None;encoded_script=None;
	keycode_map=None;layout_map=None;last_command=None;
	def __init__(self, params=dict()):
		self.last_command = "";
		self.keyboard_file = params["-l"] if "-l" in params.keys() else "{0}/duckencoder_maps.json".format(os.path.dirname(__file__));
		self.input_file = params["-i"] if "-i" in params.keys() else "./payload.txt";
		self.output_file = params["-o"] if "-o" in params.keys() else "./inject.bin";
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
		self.encoded_script = bytearray();
		raw_json = None;
		with open(self.keyboard_file, "r") as fh: raw_json = fh.read();
		jobj = json.loads(raw_json);
		self.keycode_map = jobj["keycode_map"] if "keycode_map" in jobj.keys() else {};
		self.layout_map = jobj["layout_map"] if "layout_map" in jobj.keys() else {}
	def add_null(self): self.encoded_script.append(0x00)
	def add_bytes(self, b):
		for x in b: 
			self.encoded_script.append(x);
		if (len(b) % 2 != 0): self.add_null();
	def inject_delay(self, delay):
		delay_value = delay;
		while (delay_value != 0):
			self.add_null();
			if (delay_value > 255): self.encoded_script.append(int("0xFF", 16)); delay_value -= 255;
			else: self.encoded_script.append(delay_value); delay_value = 0;
	def char_to_bytes(self, c): 
		if ord(c) < 128: return self.code_to_bytes("ASCII_{0}".format(hex(ord(c))));
		elif ord(c) < 256: return self.code_to_bytes("ISO_8859_1_{0}".format(hex(ord(c))));
		else: return self.code_to_bytes("UNICODE_{0}".format(hex(ord(c))));
	def code_to_bytes(self, a):
		results = bytearray();
		if a.replace("0x", "") not in self.layout_map.keys(): 
			results.append(int("0x00", 16));
		else:
			for b in self.layout_map[a.replace("0x", "")].split(","):
				key = b.strip();
				if key in self.keycode_map.keys(): 
					results.append(self.str_to_byte(self.keycode_map[key].strip()));
				elif key in self.layout_map.keys(): 
					results.append(self.str_to_byte(self.layout_map[key].strip()));
				else: results.append(int("0x00", 16));
		return results;
	def str_to_byte(self, a): return int(a[2:], 16) if "0x" in a else int(a);

	## wip
	def str_instr_to_byte(self, command):
		if "KEY_{0}".format(command) in self.keycode_map.keys(): 
			return self.str_to_byte(self.keycode_map["KEY_{0}".format(command)]);
		if (command == "ESCAPE"): return self.str_instr_to_byte("ESC");
		elif (command == "DEL"): return self.str_instr_to_byte("DELETE");
		elif (command == "BREAK"): return self.str_instr_to_byte("PAUSE");
		elif (command == "CONTROL"): return self.str_instr_to_byte("CTRL");
		elif (command == "DOWNARROW"): return self.str_instr_to_byte("DOWN");
		elif (command == "UPARROW"): return self.str_instr_to_byte("UP");
		elif (command == "LEFTARROW"): return self.str_instr_to_byte("LEFT");
		elif (command == "RIGHTARROW"): return self.str_instr_to_byte("RIGHT");
		elif (command == "MENU"): return self.str_instr_to_byte("APP");
		elif (command == "WINDOWS"): return self.str_instr_to_byte("GUI");
		elif (command == "PLAY" or command == "PAUSE"): return self.str_instr_to_byte("MEDIA_PLAY_PAUSE");
		elif (command == "STOP"): return self.str_instr_to_byte("MEDIA_STOP");
		elif (command == "MUTE"): return self.str_instr_to_byte("MEDIA_MUTE");
		elif (command == "VOLUMEUP"): return self.str_instr_to_byte("MEDIA_VOLUME_INC");
		elif (command == "VOLUMEDOWN"): return self.str_instr_to_byte("MEDIA_VOLUME_DEC");
		elif (command == "SCROLLLOCK"): return self.str_instr_to_byte("SCROLL_LOCK");
		elif (command == "NUMLOCK"): return self.str_instr_to_byte("NUM_LOCK");
		elif (command == "CAPSLOCK"): return self.str_instr_to_byte("CAPS_LOCK");
		else: return self.char_to_bytes(command[0][0]);
	def invoke(self):
		assert self.input_file != "" and os.path.exists(self.input_file), "Input file cannot be empty and must exist...";
		assert self.output_file != "" and os.path.exists(os.path.realpath(os.path.dirname(self.output_file))), "Output file cannot be empty and must be valid...";
		default_delay = True; default_delay_value = 255; repeat = False; repeat_count = 1
		try:
			with open(self.input_file, "r") as fh:
				line = fh.readline();
				while (line.strip() != ""):
					comps = line.split(" ", 1);
					if (comps[0] == "REM" or comps[0] == "LED" or comps[0] == "\n" or (repeat and comps[0] == "REPEAT") or  (len(comps) > 1 and comps[0][0:2] == "//")): 
						line = fh.readline(); continue;					
					if (comps[0] == "REPEAT"):
						repeat_count = int(comps[1].strip());
						comps = self.last_command.split(" ");
						repeat = True;

					## Encode line
					op = comps[0].strip();
					command = comps[1].strip();
					for i in range(0, repeat_count):
						if (op == "DEFAULT_DELAY" or op == "DEFAULTDELAY"):
							default_delay = False; default_delay_value = int(command);
						elif (op == "DELAY"):
							default_delay = False; delay_value = int(command); self.inject_delay(delay_value);
						elif (op == "STRING"):
							for c in comps[1]: self.add_bytes(self.char_to_bytes(c));
						elif (op == "STRING_DELAY"):
							delay_value = int(comps[1]);
							for c in comps[2]: self.add_bytes(self.char_to_bytes(c)); self.inject_delay(delay_value);
						elif (op == "CONTROL" or op == "CTRL"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_CTRL"]));
							else:
								self.encoded_script.append(self.str_to_byte(self.keycode_map["KEY_LEFT_CTRL"]));
								self.add_null();
						elif (op == "ALT"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps))
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_ALT"]));
							else:
								self.encoded_script.append(self.str_to_byte(self.keycode_map["KEY_LEFT_ALT"]));
								self.add_null();
						elif (op == "SHIFT"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_SHIFT"]));
							else:
								self.encoded_script.append(self.str_to_byte(self.keycode_map["KEY_LEFT_SHIFT"]));
								self.add_null();
						elif (op == "CTRL-ALT"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_CTRL"]) | self.str_to_byte(self.keycode_map["MODIFIERKEY_ALT"]));
							else: continue;
						elif (op == "CTRL-SHIFT"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_CTRL"]) | self.str_to_byte(self.keycode_map["MODIFIERKEY_SHIFT"]));
							else: continue;
						elif (op == "COMMAND-OPTION"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_KEY_LEFT_GUI"]) | self.str_to_byte(self.keycode_map["MODIFIERKEY_ALT"]));
							else: continue;
						elif (op == "ALT-SHIFT"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_KEY_LEFT_ALT"]) | self.str_to_byte(self.keycode_map["MODIFIERKEY_SHIFT"]));
							else:
								self.encoded_script.append(self.str_to_byte(self.keycode_map["KEY_LEFT_ALT"]));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_LEFT_ALT"]) | self.str_to_byte(self.keycode_map["MODIFIERKEY_SHIFT"]));
						elif (op == "ALT-TAB"):
							if (len(comps) == 1):
								self.encoded_script.append(self.str_to_byte(self.keycode_map["KEY_TAB"]));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_LEFT_GUI"]));
							else: continue;
						elif (op == "WINDOWS" or op == "GUI"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_instr_to_byte(comps[1].strip()));
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_LEFT_GUI"]));
							else: 
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_LEFT_GUI"]));
								self.add_null();
						elif (op == "COMMAND"):
							if (len(comps) > 1):
								self.encoded_script.append(self.str_to_byte(self.keycode_map["MODIFIERKEY_LEFT_GUI"]));
								self.encoded_script.append(self.str_instr_to_byte(comps[1]));
							else:
								self.encoded_script.append(self.str_to_byte(self.keycode_map["KEY_COMMAND"]));
								self.add_null();
						else: self.encoded_script.append(self.str_instr_to_byte(comps[0].strip(" ")));
						if (not default_delay and default_delay_value > 0): self.inject_delay(default_delay_value);
					if not repeat: self.last_command = line;
					line = fh.readline();
		except IOError as ex: print("Failed to read input file... {0}".format(ex)); sys.exit(-2);

		## Write final script
		if (self.debug):
			print("{0}".format(self.encoded_script));
		else:
			try:
				with open(self.output_file, "wb") as fh: fh.write(self.encoded_script);
			except Exception as ex: print("Failed to write bin file...{0}".format(ex)); sys.exit(-4);
		print("Encoder finished without error.  Please copy inject.bin to Rubber Ducky.");
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = DuckyEncoder(params);
	session.invoke();
	pass;

