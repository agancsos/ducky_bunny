#!/usr/bin/env python3
###############################################################################
# Name         : duckencoder.py                                               #
# Author       : Abel Gancsos                                                 #
# Version      : v. 1.0.0.0                                                   #
# Description  : Encodes a bin file for use with a USB Rubber Ducky.          #
###############################################################################
import os, sys;

class DuckyEncoder:
	keyboard_file=None;input_file=None;output_file=None;debug=None;encoded_script=None;keycode_map=None;keyboard_layout=None;generate=None;last_command=None;mac_mode=None;
	def __init__(self, params=dict()):
		self.last_command = "";
		self.keyboard_file = params["-l"] if "-l" in params.keys() else "";
		self.input_file = params["-i"] if "-i" in params.keys() else "./payload.txt";
		self.output_file = params["-o"] if "-o" in params.keys() else "./inject.bin";
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
		self.generate = True if "--gen" in params.keys() and int(params["--gen"]) > 0 else False;
		self.mac_mode = True if "--osx" in params.keys() and int(params["--osx"]) > 0 else False
		self.encoded_script = bytearray();
		self.keycode_map = {
			"KEY_SPACE"						     : "ASCII_20",
			"KEY_1, MODIFIERKEY_SHIFT"		     : "ASCII_21",
			"KEY_QUOTE, MODIFIERKEY_SHIFT"	     : "ASCII_22",
			"KEY_3, MODIFIERKEY_SHIFT"		     : "ASCII_23",
			"KEY_4, MODIFIERKEY_SHIFT"		     : "ASCII_24",
			"KEY_5, MODIFIERKEY_SHIFT"		     : "ASCII_25",
			"KEY_7, MODIFIERKEY_SHIFT"		     : "ASCII_26",
			"KEY_QUOTE"						     : "ASCII_27",
			"KEY_9, MODIFIERKEY_SHIFT"		     : "ASCII_28",
			"KEY_0, MODIFIERKEY_SHIFT"		     : "ASCII_29",
			"KEY_8, MODIFIERKEY_SHIFT"		     : "ASCII_2A",
			"KEY_EQUAL, MODIFIERKEY_SHIFT"	     : "ASCII_2B",
			"KEY_COMMA"						     : "ASCII_2C",
			"KEY_MINUS"						     : "ASCII_2D",
			"KEY_PERIOD"					     : "ASCII_2E",
			"KEY_SLASH"						     : "ASCII_2F",
			"KEY_0"							     : "ASCII_30",
			"KEY_1"							     : "ASCII_31",
			"KEY_2"							     : "ASCII_32",
			"KEY_3"							     : "ASCII_33",
			"KEY_4"							     : "ASCII_34",
			"KEY_5"							     : "ASCII_35",
			"KEY_6"							     : "ASCII_36",
			"KEY_7"							     : "ASCII_37",
			"KEY_8"							     : "ASCII_38",
			"KEY_9"							     : "ASCII_39",
			"KEY_SEMICOLON, MODIFIERKEY_SHIFT"   : "ASCII_3A",
			"KEY_SEMICOLON"					     : "ASCII_3B",
			"KEY_COMMA, MODIFIERKEY_SHIFT"	     : "ASCII_3C",
			"KEY_EQUAL"						     : "ASCII_3D",
			"KEY_PERIOD, MODIFIERKEY_SHIFT"	     : "ASCII_3E",
			"KEY_SLASH, MODIFIERKEY_SHIFT"	     : "ASCII_3F",
			"KEY_2, MODIFIERKEY_SHIFT"		     : "ASCII_40",
			"KEY_A, MODIFIERKEY_SHIFT"		     : "ASCII_41",
			"KEY_B, MODIFIERKEY_SHIFT"		     : "ASCII_42",
			"KEY_C, MODIFIERKEY_SHIFT"		     : "ASCII_43",
			"KEY_D, MODIFIERKEY_SHIFT"		     : "ASCII_44",
			"KEY_E, MODIFIERKEY_SHIFT"		     : "ASCII_45",
			"KEY_F, MODIFIERKEY_SHIFT"		     : "ASCII_46",
			"KEY_G, MODIFIERKEY_SHIFT"		     : "ASCII_47",
			"KEY_H, MODIFIERKEY_SHIFT"		     : "ASCII_48",
			"KEY_I, MODIFIERKEY_SHIFT"		     : "ASCII_49",
			"KEY_J, MODIFIERKEY_SHIFT"		     : "ASCII_4A",
			"KEY_K, MODIFIERKEY_SHIFT"		     : "ASCII_4B",
			"KEY_L, MODIFIERKEY_SHIFT"		     : "ASCII_4C",
			"KEY_M, MODIFIERKEY_SHIFT"		     : "ASCII_4D",
			"KEY_N, MODIFIERKEY_SHIFT"		     : "ASCII_4E",
			"KEY_O, MODIFIERKEY_SHIFT"		     : "ASCII_4F",
			"KEY_P, MODIFIERKEY_SHIFT"		     : "ASCII_50",
			"KEY_Q, MODIFIERKEY_SHIFT"		     : "ASCII_51",
			"KEY_R, MODIFIERKEY_SHIFT"		     : "ASCII_52",
			"KEY_S, MODIFIERKEY_SHIFT"		     : "ASCII_53",
			"KEY_T, MODIFIERKEY_SHIFT"		     : "ASCII_54",
			"KEY_U, MODIFIERKEY_SHIFT"		     : "ASCII_55",
			"KEY_V, MODIFIERKEY_SHIFT"		     : "ASCII_56",
			"KEY_W, MODIFIERKEY_SHIFT"		     : "ASCII_57",
			"KEY_X, MODIFIERKEY_SHIFT"		     : "ASCII_58",
			"KEY_Y, MODIFIERKEY_SHIFT"		     : "ASCII_59",
			"KEY_Z, MODIFIERKEY_SHIFT"		     : "ASCII_5A",
			"KEY_LEFT_BRACE"				     : "ASCII_5B",
			"KEY_BACKSLASH"					     : "ASCII_5C",
			"KEY_RIGHT_BRACE"				     : "ASCII_5D",
			"KEY_6, MODIFIERKEY_SHIFT"		     : "ASCII_5E",
			"KEY_MINUS, MODIFIERKEY_SHIFT"	     : "ASCII_5F",
			"KEY_TILDE"						     : "ASCII_60",
			"KEY_A"							     : "ASCII_61",
			"KEY_B"							     : "ASCII_62",
			"KEY_C"							     : "ASCII_63",
			"KEY_D"							     : "ASCII_64",
			"KEY_E"							     : "ASCII_65",
			"KEY_F"							     : "ASCII_66",
			"KEY_G"							     : "ASCII_67",
			"KEY_H"							     : "ASCII_68",
			"KEY_I"							     : "ASCII_69",
			"KEY_J"							     : "ASCII_6A",
			"KEY_K"							     : "ASCII_6B",
			"KEY_L"							     : "ASCII_6C",
			"KEY_M"							     : "ASCII_6D",
			"KEY_N"							     : "ASCII_6E",
			"KEY_O"							     : "ASCII_6F",
			"KEY_P"							     : "ASCII_70",
			"KEY_Q"							     : "ASCII_71",
			"KEY_R"							     : "ASCII_72",
			"KEY_S"							     : "ASCII_73",
			"KEY_T"							     : "ASCII_74",
			"KEY_U"							     : "ASCII_75",
			"KEY_V"							     : "ASCII_76",
			"KEY_W"							     : "ASCII_77",
			"KEY_X"							     : "ASCII_78",
			"KEY_Y"							     : "ASCII_79",
			"KEY_Z"							     : "ASCII_7A",
			"KEY_LEFT_BRACE, MODIFIERKEY_SHIFT"  : "ASCII_7B",
			"KEY_BACKSLASH, MODIFIERKEY_SHIFT"   : "ASCII_7C",
			"KEY_RIGHT_BRACE, MODIFIERKEY_SHIFT" : "ASCII_7D",
			"KEY_TILDE, MODIFIERKEY_SHIFT"	     : "ASCII_7E",
			"KEY_BACKSPACE"					     : "ASCII_7F"
		};
		self.keyboard_layout = {
			"MODIFIERKEY_CTRL"		    :  "0x01",
			"MODIFIERKEY_SHIFT"		    :  "0x02",
			"MODIFIERKEY_ALT"		    :  "0x04",
			"MODIFIERKEY_GUI"		    :  "0x08",
			"MODIFIERKEY_LEFT_CTRL"	    :  "0x01",
			"MODIFIERKEY_LEFT_SHIFT"	:  "0x02",
			"MODIFIERKEY_LEFT_ALT"	    :  "0x04",
			"MODIFIERKEY_LEFT_GUI"	    :  "0x08",
			"MODIFIERKEY_RIGHT_CTRL"	:  "0x10",
			"MODIFIERKEY_RIGHT_SHIFT"   :  "0x20",
			"MODIFIERKEY_RIGHT_ALT"	    :  "0x40",
			"MODIFIERKEY_RIGHT_GUI"	    :  "0x80",
			"KEY_MEDIA_VOLUME_INC"	    :  "0x80",
			"KEY_MEDIA_VOLUME_DEC"	    :  "0x81",
			"KEY_MEDIA_MUTE"		    :  "0x7F",
			"KEY_MEDIA_PLAY_PAUSE"	    :  "0x08",
			"KEY_MEDIA_NEXT_TRACK"	    :  "0x10",
			"KEY_MEDIA_PREV_TRACK"	    :  "0x20",
			"KEY_MEDIA_STOP"		    :  "0x40",
			"KEY_MEDIA_EJECT"		    :  "0x80",
			"KEY_A"					    :  "4",
			"KEY_B"					    :  "5",
			"KEY_C"					    :  "6",
			"KEY_D"					    :  "7",
			"KEY_E"					    :  "8",
			"KEY_F"					    :  "9",
			"KEY_G"					    :  "10",
			"KEY_H"					    :  "11",
			"KEY_I"					    :  "12",
			"KEY_J"					    :  "13",
			"KEY_K"					    :  "14",
			"KEY_L"					    :  "15",
			"KEY_M"					    :  "16",
			"KEY_N"					    :  "17",
			"KEY_O"					    :  "18",
			"KEY_P"					    :  "19",
			"KEY_Q"					    :  "20",
			"KEY_R"					    :  "21",
			"KEY_S"					    :  "22",
			"KEY_T"					    :  "23",
			"KEY_U"					    :  "24",
			"KEY_V"					    :  "25",
			"KEY_W"					    :  "26",
			"KEY_X"					    :  "27",
			"KEY_Y"					    :  "28",
			"KEY_Z"					    :  "29",
			"KEY_1"					    :  "30",
			"KEY_2"					    :  "31",
			"KEY_3"					    :  "32",
			"KEY_4"					    :  "33",
			"KEY_5"					    :  "34",
			"KEY_6"					    :  "35",
			"KEY_7"					    :  "36",
			"KEY_8"					    :  "37",
			"KEY_9"					    :  "38",
			"KEY_0"					    :  "39",
			"KEY_ENTER"				    :  "40",
			"KEY_ESC"				    :  "41",
			"KEY_BACKSPACE"			    :  "42",
			"KEY_TAB"				    :  "43",
			"KEY_SPACE"				    :  "44",
			"KEY_MINUS"				    :  "45",
			"KEY_EQUAL"				    :  "46",
			"KEY_LEFT_BRACE"			:  "47",
			"KEY_RIGHT_BRACE"		    :  "48",
			"KEY_BACKSLASH"			    :  "49",
			"KEY_NON_US_NUM"			:  "50",
			"KEY_SEMICOLON"			    :  "51",
			"KEY_QUOTE"				    :  "52",
			"KEY_TILDE"				    :  "53",
			"KEY_COMMA"				    :  "54",
			"KEY_PERIOD"				:  "55",
			"KEY_SLASH"				    :  "56",
			"KEY_CAPS_LOCK"			    :  "57",
			"KEY_F1"					:  "58",
			"KEY_F2"					:  "59",
			"KEY_F3"					:  "60",
			"KEY_F4"					:  "61",
			"KEY_F5"					:  "62",
			"KEY_F6"					:  "63",
			"KEY_F7"					:  "64",
			"KEY_F8"					:  "65",
			"KEY_F9"					:  "66",
			"KEY_F10"				    :  "67",
			"KEY_F11"				    :  "68",
			"KEY_F12"				    :  "69",
			"KEY_PRINTSCREEN"		    :  "70",
			"KEY_SCROLL_LOCK"		    :  "71",
			"KEY_PAUSE"				    :  "72",
			"KEY_INSERT"				:  "73",
			"KEY_HOME"				    :  "74",
			"KEY_PAGEUP"				:  "75",
			"KEY_DELETE"				:  "76",
			"KEY_END"				    :  "77",
			"KEY_PAGEDOWN"			    :  "78",
			"KEY_RIGHT"				    :  "79",
			"KEY_LEFT"				    :  "80",
			"KEY_DOWN"				    :  "81",
			"KEY_UP"					:  "82",
			"KEY_NUM_LOCK"			    :  "83",
			"KEYPAD_SLASH"			    :  "84",
			"KEYPAD_ASTERIX"			:  "85",
			"KEYPAD_MINUS"			    :  "86",
			"KEYPAD_PLUS"			    :  "87",
			"KEYPAD_ENTER"			    :  "88",
			"KEYPAD_EQUALS"			    :  "103",
			"KEYPAD_1"				    :  "89",
			"KEYPAD_2"				    :  "90",
			"KEYPAD_3"				    :  "91",
			"KEYPAD_4"				    :  "92",
			"KEYPAD_5"				    :  "93",
			"KEYPAD_6"				    :  "94",
			"KEYPAD_7"				    :  "95",
			"KEYPAD_8"				    :  "96",
			"KEYPAD_9"				    :  "97",
			"KEYPAD_0"				    :  "98",
			"KEYPAD_PERIOD"			    :  "99",
			"KEY_APP"				    :  "0x65",
			"KEY_POWER"				    :  "0x66",
			"KEY_EXE"				    :  "0x74",
			"KEY_HELP"				    :  "0x75",
			"KEY_MENU"				    :  "0x76",
			"KEY_SELECT"				:  "0x77",
			"KEY_STOP"				    :  "0x78",
			"KEY_AGAIN"				    :  "0x79",
			"KEY_UNDO"				    :  "0x7A",
			"KEY_CUT"				    :  "0x7B",
			"KEY_COPY"				    :  "0x7C",
			"KEY_PASTE"				    :  "0x7D",
			"KEY_FIND"				    :  "0x7E",
			"KEY_SYSTEM_POWER"		    :  "0x81",
			"KEY_SYSTEM_SLEEP"		    :  "0x82",
			"KEY_SYSTEM_WAKE"		    :  "0x83",
			"KEYPAD_PIPE"			    :  "0xC9",
			"KEY_LEFT_CTRL"			    :  "0xE0",
			"KEY_LEFT_SHIFT"			:  "0xE1",
			"KEY_LEFT_ALT"			    :  "0xE2",
			"KEY_LEFT_GUI"			    :  "0xE3",
			"KEY_COMMAND"			    :  "0xE3",
			"KEY_RIGHT_CTRL"			:  "0xE4",
			"KEY_RIGHT_SHIFT"		    :  "0xE5",
			"KEY_RIGHT_ALT"			    :  "0xE6",
			"KEY_RIGHT_GUI"			    :  "0xE7"
		};
		self.load_keyboard_layout();
	def load_keyboard_layout(self):
		if (self.keyboard_file != "" and os.path.exists(self.keyboard_file)):
			try:
				with open(self.keyboard_file, "r") as fh:
					line = fh.readline();
					while (line != ""):
						comps = line.split("=");
						if (line == "\n" or len(comps) < 2 or line[:1] == "/"): line = fh.readline(); continue;
						self.keycodeMap[comps[1].strip("					").strip(" ")] = comps[0].strip(" ");
						if (self.generate): print("\"{0}\":\"{1}\",".format(comps[1].strip("					").strip(" ")));
						line = fh.readline();
			except Exception: print("Failed to read keyboard file.  Will use default keycode map...");
	def add_null(self):
		if (self.mac_mode): self.encoded_script.append(0x02);
		else: self.encoded_script.append(0x00)
	def add_bytes(self, b):
		for x in b: self.encoded_script.append(x);
		if (len(b) % 2 != 0): self.add_null();
	def inject_delay(self, delay):
		delay_value = delay;
		while (delay_value != 0):
			self.add_null();
			if (delay_value > 255): self.encoded_script.append(int(0xFF, 16)); delay_value -= 255;
			else: self.encoded_script.append(delay_value); delay_value = 0;
	def char_to_bytes(self, c): return self.code_to_bytes(c);
	def code_to_bytes(self, a):
		results = bytearray();
		for b in a:
			if self.keyboard_layout.keys().__contains__("KEY_{0}".format(b)):
				for c in self.keyboard_layout["KEY_{0}".format(b)].split(","):
					results.append(self.str_to_byte(c));
			elif b in self.keycode_map.keys():
				for c in self.keycode_map[b].split(","): results.append(self.str_to_byte(c));
		return results;
	def str_to_byte(self, a):
		if "0x" in a: return int(a.replace("0x", "", 16));  
		else: return int(a); 
	def str_instr_to_byte(self, command):
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
		else:
			if command in self.keyboard_layout: self.add_bytes(self.code_to_bytes(command));
			else:
				for k in self.keycode_map:
					if "KEY_{0}".format(command[0]) in k.split(", "): return self.char_to_bytes(self.keycode_map[k].replace("ASCII_", ""))[0];
			return self.char_to_bytes(command)[0];
	def invoke(self):
		assert self.input_file != "" and os.path.exists(self.input_file), "Input file cannot be empty and must exist...";
		assert self.output_file != "" and os.path.exists(os.path.realpath(os.path.dirname(self.output_file))), "Output file cannot be empty and must be valid...";
		default_delay = True; default_delay_value = 255; repeat = False; repeat_count = 1
		try:
			with open(self.input_file, "r") as fh:
				line = fh.readline();
				while (line != ""):
					comps = line.split(" ");
					if (comps[0] == "REM" or comps[0] == "LED" or comps[0] == "\n" or (repeat and comps[0] == "REPEAT") or  (len(comps) > 1 and comps[0][0:2] == "//")): continue;
					if (self.debug): print(line);
					
					if (comps[0] == "REPEAT"):
						repeat_count = int(comps[1].strip());
						comps = self.last_command.split(" ");
						repeat = True;

					## Encode line
					command = " ".join(comps[1:]).strip() if len(comps) > 1 else comps[0].strip();
					op = comps[0].strip();
					for i in range(0, repeat_count):
						if (op == "DEFAULT_DELAY" or op == "DEFAULTDELAY"):
							default_delay = False; default_delay_value = int(command);
						elif (op == "DELAY"):
							default_delay = False; delay_value = int(command); self.inject_delay(delay_value);
						elif (op == "STRING"):
							for c in command: self.add_bytes(self.char_to_bytes(c));
						elif (op == "STRING_DELAY"):
							delay_value = int(comps[1]);
							for c in comps[2]: self.add_bytes(self.char_to_bytes(c)); self.inject_delay(delay_value);
						elif (op == "CONTROL" or op == "CTRL"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_CTRL"]));
							else:
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["KEY_LEFT_CTRL"]));
								self.add_null();
						elif (op == "ALT"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command))
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_ALT"]));
							else:
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["KEY_LEFT_ALT"]));
								self.add_null();
						elif (op == "SHIFT"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_SHIFT"]));
							else:
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["KEY_LEFT_SHIFT"]));
								self.add_null();
						elif (op == "CTRL-ALT"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_CTRL"]) | self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_ALT"]));
							else: continue;
						elif (op == "CTRL-SHIFT"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_CTRL"]) | self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_SHIFT"]));
							else: continue;
						elif (op == "COMMAND-OPTION"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_KEY_LEFT_GUI"]) | self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_ALT"]));
							else: continue;
						elif (op == "ALT-SHIFT"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_KEY_LEFT_ALT"]) | self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_SHIFT"]));
							else:
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["KEY_LEFT_ALT"]));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_LEFT_ALT"]) | self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_SHIFT"]));
						elif (op == "ALT-TAB"):
							if (len(command) == 1):
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["KEY_TAB"]));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_LEFT_GUI"]));
							else: continue;
						elif (op == "WINDOWS" or op == "GUI"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_GUI"]));
							else: 
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_LEFT_GUI"]));
								self.add_null();
						elif (op == "COMMAND"):
							if (len(command) > 1):
								self.encoded_script.append(self.str_instr_to_byte(command));
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["MODIFIERKEY_LEFT_GUI"]));
							else:
								self.encoded_script.append(self.str_instr_to_byte(self.keyboard_layout["KEY_COMMAND"]));
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

