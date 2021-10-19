package main
import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

// Globals
var APPLICATION_NAME    = "Ducky Encoder";
var APPLICATION_AUTHOR  = "Abel Gancsos";
var APPLICATION_VERSION = "1.0.0.0";
var APPLICATION_FLAGS   = map[string]string {
	"-h"              : "Prints the help menu",
	"-i"              : "Full path to the input Ducky script file",
	"-o"              : "Full path to the output inject file (default: ./inject.bin)",
	"-l"              : "Full path to the keyboard file",
	"--debug"         : "Don't modify the file system",
};
/*****************************************************************************/

// Main
func main() {
	var params = map[string]string{};
	for i := 0; i < len(os.Args); i++ {
		if len(os.Args) - 1 < i + 1 || string(strings.Split(os.Args[i + 1], " ")[0][0]) == "-" {
			params[os.Args[i]] = "";
		} else {
			params[os.Args[i]] = os.Args[i + 1];
		}
	}
	var temp, _ = strconv.Atoi(params["-h"]);
	if temp > 0 {
		HelpMenu();
		os.Exit(0);
	}
	var session = NewEncoder(params);
	session.Encode();
	os.Exit(0);
}
/*****************************************************************************/


// Encoder
type Encoder struct {
	inputFilePath         string
	outputFilePath        string
	keyboardFilePath      string
	keycodeMap            map[string]string
	debug                 bool
	generate              bool
}
func NewEncoder(params map[string]string) *Encoder {
	var instance = &Encoder{};
	instance.inputFilePath = "./payload.txt";
	instance.outputFilePath = "./inject.bin";
	instance.debug = false;
	if params["-i"] != "" { instance.inputFilePath = params["-i"]; }
	if params["-o"] != "" { instance.outputFilePath = params["-o"]; }
	if params["-l"] != "" { instance.keyboardFilePath = params["-l"]; }
	_, instance.debug = params["--debug"];
	_, instance.generate = params["--gen"];
	instance.keycodeMap = map[string]string {
		"KEY_SPACE"                          : "ASCII_20",
		"KEY_1, MODIFIERKEY_SHIFT"           : "ASCII_21",
		"KEY_QUOTE, MODIFIERKEY_SHIFT"       : "ASCII_22",
		"KEY_3, MODIFIERKEY_SHIFT"           : "ASCII_23",
		"KEY_4, MODIFIERKEY_SHIFT"           : "ASCII_24",
		"KEY_5, MODIFIERKEY_SHIFT"           : "ASCII_25",
		"KEY_7, MODIFIERKEY_SHIFT"           : "ASCII_26",
		"KEY_QUOTE"                          : "ASCII_27",
		"KEY_9, MODIFIERKEY_SHIFT"           : "ASCII_28",
		"KEY_0, MODIFIERKEY_SHIFT"           : "ASCII_29",
		"KEY_8, MODIFIERKEY_SHIFT"           : "ASCII_2A",
		"KEY_EQUAL, MODIFIERKEY_SHIFT"       : "ASCII_2B",
		"KEY_COMMA"                          : "ASCII_2C",
		"KEY_MINUS"                          : "ASCII_2D",
		"KEY_PERIOD"                         : "ASCII_2E",
		"KEY_SLASH"                          : "ASCII_2F",
		"KEY_0"                              : "ASCII_30",
		"KEY_1"                              : "ASCII_31",
		"KEY_2"                              : "ASCII_32",
		"KEY_3"                              : "ASCII_33",
		"KEY_4"                              : "ASCII_34",
		"KEY_5"                              : "ASCII_35",
		"KEY_6"                              : "ASCII_36",
		"KEY_7"                              : "ASCII_37",
		"KEY_8"                              : "ASCII_38",
		"KEY_9"                              : "ASCII_39",
		"KEY_SEMICOLON, MODIFIERKEY_SHIFT"   : "ASCII_3A",
		"KEY_SEMICOLON"                      : "ASCII_3B",
		"KEY_COMMA, MODIFIERKEY_SHIFT"       : "ASCII_3C",
		"KEY_EQUAL"                          : "ASCII_3D",
		"KEY_PERIOD, MODIFIERKEY_SHIFT"      : "ASCII_3E",
		"KEY_SLASH, MODIFIERKEY_SHIFT"       : "ASCII_3F",
		"KEY_2, MODIFIERKEY_SHIFT"           : "ASCII_40",
		"KEY_A, MODIFIERKEY_SHIFT"           : "ASCII_41",
		"KEY_B, MODIFIERKEY_SHIFT"           : "ASCII_42",
		"KEY_C, MODIFIERKEY_SHIFT"           : "ASCII_43",
		"KEY_D, MODIFIERKEY_SHIFT"           : "ASCII_44",
		"KEY_E, MODIFIERKEY_SHIFT"           : "ASCII_45",
		"KEY_F, MODIFIERKEY_SHIFT"           : "ASCII_46",
		"KEY_G, MODIFIERKEY_SHIFT"           : "ASCII_47",
		"KEY_H, MODIFIERKEY_SHIFT"           : "ASCII_48",
		"KEY_I, MODIFIERKEY_SHIFT"           : "ASCII_49",
		"KEY_J, MODIFIERKEY_SHIFT"           : "ASCII_4A",
		"KEY_K, MODIFIERKEY_SHIFT"           : "ASCII_4B",
		"KEY_L, MODIFIERKEY_SHIFT"           : "ASCII_4C",
		"KEY_M, MODIFIERKEY_SHIFT"           : "ASCII_4D",
		"KEY_N, MODIFIERKEY_SHIFT"           : "ASCII_4E",
		"KEY_O, MODIFIERKEY_SHIFT"           : "ASCII_4F",
		"KEY_P, MODIFIERKEY_SHIFT"           : "ASCII_50",
		"KEY_Q, MODIFIERKEY_SHIFT"           : "ASCII_51",
		"KEY_R, MODIFIERKEY_SHIFT"           : "ASCII_52",
		"KEY_S, MODIFIERKEY_SHIFT"           : "ASCII_53",
		"KEY_T, MODIFIERKEY_SHIFT"           : "ASCII_54",
		"KEY_U, MODIFIERKEY_SHIFT"           : "ASCII_55",
		"KEY_V, MODIFIERKEY_SHIFT"           : "ASCII_56",
		"KEY_W, MODIFIERKEY_SHIFT"           : "ASCII_57",
		"KEY_X, MODIFIERKEY_SHIFT"           : "ASCII_58",
		"KEY_Y, MODIFIERKEY_SHIFT"           : "ASCII_59",
		"KEY_Z, MODIFIERKEY_SHIFT"           : "ASCII_5A",
		"KEY_LEFT_BRACE"                     : "ASCII_5B",
		"KEY_BACKSLASH"                      : "ASCII_5C",
		"KEY_RIGHT_BRACE"                    : "ASCII_5D",
		"KEY_6, MODIFIERKEY_SHIFT"           : "ASCII_5E",
		"KEY_MINUS, MODIFIERKEY_SHIFT"       : "ASCII_5F",
		"KEY_TILDE"                          : "ASCII_60",
		"KEY_A"                              : "ASCII_61",
		"KEY_B"                              : "ASCII_62",
		"KEY_C"                              : "ASCII_63",
		"KEY_D"                              : "ASCII_64",
		"KEY_E"                              : "ASCII_65",
		"KEY_F"                              : "ASCII_66",
		"KEY_G"                              : "ASCII_67",
		"KEY_H"                              : "ASCII_68",
		"KEY_I"                              : "ASCII_69",
		"KEY_J"                              : "ASCII_6A",
		"KEY_K"                              : "ASCII_6B",
		"KEY_L"                              : "ASCII_6C",
		"KEY_M"                              : "ASCII_6D",
		"KEY_N"                              : "ASCII_6E",
		"KEY_O"                              : "ASCII_6F",
		"KEY_P"                              : "ASCII_70",
		"KEY_Q"                              : "ASCII_71",
		"KEY_R"                              : "ASCII_72",
		"KEY_S"                              : "ASCII_73",
		"KEY_T"                              : "ASCII_74",
		"KEY_U"                              : "ASCII_75",
		"KEY_V"                              : "ASCII_76",
		"KEY_W"                              : "ASCII_77",
		"KEY_X"                              : "ASCII_78",
		"KEY_Y"                              : "ASCII_79",
		"KEY_Z"                              : "ASCII_7A",
		"KEY_LEFT_BRACE, MODIFIERKEY_SHIFT"  : "ASCII_7B",
		"KEY_BACKSLASH, MODIFIERKEY_SHIFT"   : "ASCII_7C",
		"KEY_RIGHT_BRACE, MODIFIERKEY_SHIFT" : "ASCII_7D",
		"KEY_TILDE, MODIFIERKEY_SHIFT"       : "ASCII_7E",
		"KEY_BACKSPACE"                      : "ASCII_7F",
	};
	if instance.keyboardFilePath != "" { instance.extractKeycodes(); }
	return instance;
}
func (x Encoder) charToByte(c string) byte {
	var intVal, _ = strconv.Atoi(c);
	return byte(intVal);
}
func (x Encoder) strToByte(str string) byte {
	if strings.HasPrefix(str, "0x") {
		var temp, _ = strconv.ParseInt(str[2:], 0, 16);
		return byte(temp);
	} else {
		var temp, _ = strconv.ParseInt(str, 0, 0);
		return byte(temp);
	}
}
func (x Encoder) Encode() {
	var rawDuckyScript, err = ioutil.ReadFile(x.inputFilePath);
	var duckyScript = string(rawDuckyScript);
	if err != nil && !x.debug {
		println("Failed to read input file...");
		os.Exit(-2);
	} else{
		var encodedScript []byte;
		var duckyLines = strings.Split(duckyScript, "\n");
		var defaultDelay = true;
		var defaultDelayOverrideValue = 255;
		for _, line := range duckyLines {
			var comps = strings.Split(line, " ");

			// Skips and corrections
			if comps[0] == "REM" ||
				comps[0] == "LED"||
				comps[0] == "\n" { continue; }
			if x.debug { println(line); }

			// Encode line
			var command = "";
			if len(comps) > 1 {
				command = strings.Trim(comps[1], " ");
			} else { command = strings.Trim(comps[0], " "); }
			switch (strings.Trim(comps[0], " ")) {
				case "DEFAULT_DELAY", "DEFAULTDELAY":
					defaultDelay = false;
					defaultDelayOverrideValue, _ = strconv.Atoi(command);
					break;
				case "DELAY":
					defaultDelay = false;
					var delayValue, _ = strconv.Atoi(command);
					for ; delayValue > 0; {
						encodedScript = append(encodedScript, byte(0x00));
						if (delayValue > 255) {
							encodedScript = append(encodedScript, byte(0xFF));
							delayValue -= 255;
						} else {
							encodedScript = append(encodedScript, byte(delayValue));
							delayValue = 0;
						}
					}
					break;
				case "STRING":
					for _, c := range command { encodedScript = append(encodedScript, x.charToByte(string(c))); }
					break;
				case "STRING_DELAY":
					var delayValue, _ = strconv.Atoi(comps[1]);
					for _, c := range comps[2] {
						encodedScript = append(encodedScript, x.charToByte(string(c)));
						for ; delayValue > 0; {
							encodedScript = append(encodedScript, byte(0x00));
							if (delayValue > 255) {
								encodedScript = append(encodedScript, byte(0xFF));
								delayValue -= 255;
							} else {
								encodedScript = append(encodedScript, byte(delayValue));
								delayValue = 0;
							}
						}
					}
					break;
				case "CONTROL", "CTRL":
					if len(command) > 1 {
						encodedScript = append(encodedScript, x.strInstrToByte(command));
						encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_CTRL"]));
					} else {
						encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["KEY_LEFT_CTRL"]));
						encodedScript = append(encodedScript, byte(0x00));
					}
					break;
				case "ALT":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_ALT"]));
                    } else {
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["KEY_LEFT_ALT"]));
                        encodedScript = append(encodedScript, byte(0x00));
                    }
                    break;
				case "SHIFT":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_SHIFT"]));
                    } else {
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["KEY_LEFT_SHIFT"]));
                        encodedScript = append(encodedScript, byte(0x00));
                    }
                    break;
				case "CTRL-ALT":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_CTRL"]) | x.strInstrToByte(x.keycodeMap["MODIFIERKEY_ALT"]));
                    } else { continue; }
                    break;
				case "CTRL-SHIFT":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_CTRL"]) | x.strInstrToByte(x.keycodeMap["MODIFIERKEY_SHIFT"]));
                    } else { continue; }
                    break;
				case "COMMAND-OPTION":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_KEY_LEFT_GUI"]) | x.strInstrToByte(x.keycodeMap["MODIFIERKEY_ALT"]));
                    } else { continue; }
                    break;
				case "ALT-SHIFT":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_LEFT_ALT"]) | x.strInstrToByte(x.keycodeMap["MODIFIERKEY_SHIFT"]));
                    } else {
						encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["KEY_LEFT_ALT"]));
						encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_LEFT_ALT"]) | x.strInstrToByte(x.keycodeMap["MODIFIERKEY_SHIFT"]));
					}
                    break;
				case "ALT-TAB":
                    if len(command) == 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["KEY_TAB"]));
						encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_LEFT_GUI"]));
                    } else { continue; }
                    break;
				case "WINDOWS", "GUI":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_KEY_LEFT_GUI"]))
                    } else {
						encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_KEY_LEFT_GUI"]));
						encodedScript = append(encodedScript, byte(0x00));
					}
                    break;
				case "COMMAND":
                    if len(command) > 1 {
                        encodedScript = append(encodedScript, x.strInstrToByte(command));
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["MODIFIERKEY_KEY_LEFT_GUI"]));
                    } else {
                        encodedScript = append(encodedScript, x.strInstrToByte(x.keycodeMap["KEY_COMMAND"]));
                        encodedScript = append(encodedScript, byte(0x00));
                    }
                    break;
				default:
					encodedScript = append(encodedScript, x.strToByte(strings.Trim(comps[0], " ")));
					encodedScript = append(encodedScript, byte(0x00));
					break;
			}
			if !defaultDelay && defaultDelayOverrideValue > 0 {
				var delayValue = defaultDelayOverrideValue;
				for ; delayValue > 0; {
					encodedScript = append(encodedScript, byte(0x00));
					if (delayValue > 255) {
						encodedScript = append(encodedScript, byte(0xFF));
						delayValue -= 255;
					} else {
						encodedScript = append(encodedScript, byte(delayValue));
						delayValue = 0;
					}
				}
			}
		}

		// Write final script
		if x.debug {
			println(fmt.Sprintf("Encoded script:\n%v", encodedScript));
		} else {
			var err = ioutil.WriteFile(x.outputFilePath, encodedScript, 0777);
			if err != nil {
				println("Failed to write bin file...");
				os.Exit(-4);
			}
		}

		println("Encoder finished without error.  Please copy inject.bin to Rubber Ducky.");
	}
}
func (x Encoder) strInstrToByte(command string) byte {
	if x.keycodeMap["KEY_" + command] != "" { return x.strToByte(strings.Replace(x.keycodeMap["KEY_" + command], "ASCII_", "", -1)); }
	switch (command) {
		case "ESCAPE": return x.strInstrToByte("ESC");
		case "DEL": return x.strInstrToByte("DELETE");
		case "BREAK": return x.strInstrToByte("PAUSE");
		case "CONTROL": return x.strInstrToByte("CTRL");
		case "DOWNARROW": return x.strInstrToByte("DOWN");
		case "UPARROW": return x.strInstrToByte("UP");
		case "LEFTARROW": return x.strInstrToByte("LEFT");
		case "RIGHTARROW": return x.strInstrToByte("RIGHT");
		case "MENU": return x.strInstrToByte("APP");
		case "WINDOWS": return x.strInstrToByte("GUI");
		case "PLAY", "PAUSE": return x.strInstrToByte("MEDIA_PLAY_PAUSE");
		case "STOP": return x.strInstrToByte("MEDIA_STOP");
		case "MUTE": return x.strInstrToByte("MEDIA_MUTE");
		case "VOLUMEUP": return x.strInstrToByte("MEDIA_VOLUME_INC");
		case "VOLUMEDOWN": return x.strInstrToByte("MEDIA_VOLUME_DEC");
		case "SCROLLLOCK": return x.strInstrToByte("SCROLL_LOCK");
		case "NUMLOCK": return x.strInstrToByte("NUM_LOCK");
		case "CAPSLOCK": return x.strInstrToByte("CAPS_LOCK");
		default: return x.strToByte(command);
	}
	//return "";
}
func (x *Encoder) extractKeycodes() {
	var rawKeycodes, err = ioutil.ReadFile(x.keyboardFilePath);
	if err != nil {
		println("Failed to read keyboard file.  Will use default keycode map...");
	} else {
		var lines = strings.Split(string(rawKeycodes), "\n");
		for _, line := range lines {
			var comps = strings.Split(line, "=");
			if line == "\n" ||
				len(line) == 0 ||
				line[:1] == "/" ||
				len(comps) < 2 { continue; }
			x.keycodeMap[strings.Trim(strings.Trim(comps[1], "					"), " ")] = strings.Trim(comps[0], " ");
			if x.generate { println("\"" + strings.Trim(strings.Trim(comps[1], "					"), " ") +
				"\"        : \"" + strings.Trim(comps[0], " ") + "\","); }
		}
	}
}
/*****************************************************************************/

// Helpers
func HelpMenu() {
    println(PadLeft("", 80, "#"));
    println(PadLeft("# Name     : " + APPLICATION_NAME, 79, " ") + "#");
    println(PadLeft("# Author   : " + APPLICATION_AUTHOR + "(port from Hak5)", 79, " ") + "#");
    println(PadLeft("# Version  : " + APPLICATION_VERSION, 79, " ") + "#");
    println(PadLeft("# Flags", 79, " ") + "#");
    for key, value := range APPLICATION_FLAGS {
        println(PadLeft("#  " + key + ": " + value, 79, " ") + "#");
    }
    println(PadLeft("", 80, "#"));
}

func PadLeft(str string, le int, pad string) string {
    if len(str) > le {
        return str[0:le];
    }
    result := "";
    for i := len(str); i < le; i++ {
        result += pad;
    }
    return str + result;
}
/*****************************************************************************/
