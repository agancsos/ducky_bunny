#!/usr/bin/ruby
###############################################################################
# Name             : flash_ducky.rb                                           #
# Author           : Abel Gancsos                                             #
# Version          : v. 1.0.0.0                                               #
# Description      : Helps reset a Ducky USB to work with different OS.       #
###############################################################################

class Flasher
	@base_path=nil;@platform=nil;@flasher_endpoint=nil;@dfu_path=nil;@java_path=nil;@java_version=nil;@which_cmd=nil;@flasher_platform=nil;@dfu_install=nil;@usb_id=nil;@usb_cmd=nil;@debug=nil;@no_logo=nil;
	def initialize(params={})
		@flasher_endpoint = (params["--flasher"] != nil ? params["--flasher"] : "https://github.com/hak5darren/USB-Rubber-Ducky");
		@platform = RUBY_PLATFORM;
		@base_path = Dir.pwd;
		self.set_patform_secifications();
		@java_path = (params["--java"] != nil ? params["--java"] : `#{@which_cmd} javac`.strip);
		@dfu_path = (params["--dfu"] != nil ? params["--dfu"] : `#{@which_cmd} dfu-programmer`.strip);
		@debug = (params["--debug"] != nil and params["--debug"].to_i > 0 ? true : false);
		@no_logo = (params["--no-logo"] != nil and params["--no-logo"].to_i > 0 ? true : false);
		@java_version = `#{@java_path} -version 2>&1`.strip;
	end
	def set_patform_secifications()
		@which_cmd = "which";
		case @platform
			when /darwin/i 
				@flasher_platform = "osx";
				@usb_cmd = "system_profiler SPUSBDataType";
				if (`#{@which_cmd} brew` != "")
					@dfu_install = "brew install dfu-programmer";
				end
			else
				@flasher_platform = nil;
		end
	end
	def flash()
		if (@usb_id != nil and @usb_id != "")
			`dfu-programmer #{@usb_id} erase`;
			`dfu-programmer #{@usb_id} flash --suppress-bootloader-mem #{@base_path}/USB-Rubber-Ducky/Firmware/Images/#{@flasher_platform}.hex`;
			`dfu-programmer #{@usb_id} reset`;
		end
	end
	def invoke()
		if (not @no_logo)
			print "#{"".rjust(80, "#")}\n";
			print "# Platform         : #{@platform}".ljust(79, " ") + "#\n";
			print "# Flasher Platform : #{@flasher_platform}".ljust(79, " ") + "#\n";
			print "# Working Directory: #{@base_path}".ljust(79, " ") + "#\n";
			print "# Java Path        : #{@java_path}".ljust(79, " ") + "#\n";
			print "# DFU Path         : #{@dfu_path}".ljust(79, " ") + "#\n";
			print "# Java Version     : #{@java_version}".ljust(79, " ") + "#\n";
			print "# Ducky USB ID     : #{@usb_id}".ljust(79, " ") + "#\n";
			print "# Needs Flasher    : #{@dfu_path == nil}".ljust(79, " ") + "#\n";
			print "# Needs OpenJDK    : #{@java_version == nil}".ljust(79, " ") + "#\n";
			print "#{"".rjust(80, "#")}\n";
		end

		if (@java_version != nil and @java_version != "")
			if (@dfu_path == nil or @dfu_path == "")
				if (@dfu_install != nil and @dfu_install != "")
					`brew install dfu-programmer`;
					@dfu_path = `#{@which_cmd} dfu-programmer`.strip;
				else
					print "Please install dfu-programmer manually...\n";
					exit(-1);
				end
			end
			if not @debug
				self.flash();
			end
			print "Please use duckencoder.jar (java -jar duckencoder.jar -i payload.txt) to compile your payload.txt into an inject.bin binary.\n"
		else
			print "You need an OpenJDK installation...\n";
		end
	end
end

params = {};
for i in 0..ARGV.length - 1
	params[ARGV[i]] = ARGV[i + 1];
end
session = Flasher.new(params);
session.invoke();
