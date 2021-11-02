import Foundation
import AppKit

class BunnyMonitor {
	public var volume      : String = "";
	public var payloadPath : String = "";
	public var switchNum   : String = "";
	public var isDebug     : Bool   = false;
	public var safeMode    : Bool   = false;
	public var iolock      : Bool   = false;

	public init() {
	}

	/// Decrypts files for use
	@objc func onWake(note: NSNotification) {
		if (!self.safeMode) {
			self.iolock = true;
			self.flipPayload();
			self.iolock = false;
		}
	}

	/// Encrypts files for protection
	@objc func onSleep(note: NSNotification) {
		if (!self.safeMode) {
			self.iolock = true;
			self.flipPayload();
			self.iolock = false;
		}
	}

	/// Registers with the listener to receive notifications
	private func registerNotifications() {
		NSWorkspace.shared.notificationCenter.addObserver(self, selector: #selector(onWake), name: NSWorkspace.didWakeNotification, object: nil);
		NSWorkspace.shared.notificationCenter.addObserver(self, selector: #selector(onSleep), name: NSWorkspace.willSleepNotification, object: nil);
	}

	/// Flips the current payload to the desired payload
	private func flipPayload() {
		var isDir: UnsafeMutablePointer<ObjCBool>?;
		if (FileManager.default.fileExists(atPath: self.payloadPath, isDirectory: isDir)) {
			print("Copying '\(self.payloadPath)' to '\(NSHomeDirectory())/Desktop/payload.txt'");
			if (!self.isDebug) {
				try? FileManager.default.copyItem(atPath: "\(self.payloadPath)", toPath: "\(NSHomeDirectory())/Desktop/payload.txt");
            }
		}
		else if (FileManager.default.fileExists(atPath: "\(self.volume)/payloads/\(self.switchNum)", isDirectory: isDir)) {
			print("Copying '\(NSHomeDirectory())/Desktop/payload.txt' to '\(self.volume)/payloads/\(self.switchNum)'");
			if (!self.isDebug) {
				try? FileManager.default.copyItem(atPath: "\(NSHomeDirectory())/Desktop/payload.txt", toPath: "\(self.volume)/payloads/\(self.switchNum)/payload.txt");
			}
		}	
	}

	/// Starts the watcher
	public func watch() {
		self.registerNotifications();
	}
}

let group   : DispatchGroup = DispatchGroup();
let watcher : BunnyMonitor = BunnyMonitor();
for i : Int in 0..<CommandLine.arguments.count {
	if (CommandLine.arguments[i] == "-v" || CommandLine.arguments[i] == "--volume") {
		watcher.safeMode = true;
	}
	else if (CommandLine.arguments[i] == "-p") {
		watcher.payloadPath = CommandLine.arguments[i + 1];
	}
	else if (CommandLine.arguments[i] == "--debug") {
		watcher.isDebug = true;
	}
	else if (CommandLine.arguments[i] == "-s" || CommandLine.arguments[i] == "--switch") {
		watcher.switchNum = CommandLine.arguments[i + 1];
	}
}
watcher.watch();	
RunLoop.current.run();
