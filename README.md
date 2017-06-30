# Jet changes from the original AlexaPi
	This version provides support for Neopixel type arrays with Alexa (e.g. Neopixel Ring) on the Raspberry Pi.
	Note: This has only been tested on Pi 3, you may need to change settings / pins for other Pi's.

	Status changes in Alexa are sent via a UDP socket to the server which controls the neopixel ring.  Default udp port is 9999,
	and can be set when starting the server, and in /etc/opt/AlexaPi/config.yaml (raspberrypi / neopixel_udp_port: 9999),
	ensure both server and AlexaPi have matching ports

	## Neopixel Wiring
	You will also need to install: https://github.com/jetty840/rpi_ws281x and start the server (see the github for instructions)

	Connections as follows:
		- Example: https://www.adafruit.com/product/1463
		- +3.3V Neopixel +
			- if supplying from Pi, verifying the onboard 3.3V can handle the current load from the neopixels
			- if powering from 5V, you will need logic converter for the Data line
		- GND   Neopixel -
		- Data  Gpio 21

	## Mute - Button/LED Wiring
	I've added support for an led based momentary push button to enable/disable Alexa from responding,
	(e.g. https://www.adafruit.com/product/481).  LED lit when Alexa is enabled, and not lit when disabled, pressing the
	button toggles the state, and holding it for 5 seconds reboots the pi (assuming the pi hasn't crashed).  After 5 seconds, the button
	led flashes rapidly, release the button to reboot

	The existing button support for press to listen has been removed and replaced with this.

	Connections as follows:
		- Switch Normally Open Gpio 18 (button setting in /etc/opt/AlexaPi/config.yaml)
		- Switch Common        GND
		- Neg		       Gpio 22
		- Pos		       +3.3V

	Relevant gpio's are set by "button" for the switch and "mute_light" for the led in /etc/opt/AlexaPi/config.yaml

## Installing:
	cd /opt
	git clone https://github.com/jetty840/AlexaPi
	install as per origin AlexaPi instructions




# AlexaPi (the new & awesome version) [![Gitter chat](https://badges.gitter.im/alexa-pi/Lobby.png)](https://gitter.im/alexa-pi/Lobby)

This is a client for Amazon's Alexa service. It is intended and tested to run on a wide range of platforms, such as Raspberry Pi, Orange Pi, CHIP and ordinary Linux desktops.

### Do you want to help out? Read the [Contribution Guide](CONTRIBUTING.md).

### Check out the [Documentation Wiki](https://github.com/alexa-pi/AlexaPi/wiki) and [Change Log](CHANGELOG.md).

## Requirements

You will need:

1. **A Linux box**
    - a Raspberry Pi and an SD Card with a fresh install of Raspbian
    - or an Orange Pi with Armbian
    - or pretty much any up-to-date Linux system
2. **Audio peripherals**
    - external speaker with 3.5mm Jack
    - USB Sound Dongle and microphone
3. Other
    - (optional) (Raspberry Pi) a push button connected between GPIO 18 and GND (configurable)
    - (optional) (Raspberry Pi) a dual colour LED (or 2 single LEDs) connected to GPIO 24 & 25 (configurable)

## You wanna give it a try? Check out the [Installation Guide](https://github.com/alexa-pi/AlexaPi/wiki/Installation).

## Issues / Bugs / Documentation / etc.

If your AlexaPi isn't running on startup, crashes or your audio input / output isn't working, be sure to check out:

- our **[Documentation Wiki](https://github.com/alexa-pi/AlexaPi/wiki)** - the sections with _debugging_ in their name are your friends!
- our **[Issue Tracker](https://github.com/alexa-pi/AlexaPi/issues)**. 

Also, you can
- chat with us at **[gitter.im/alexa-pi/Lobby](https://gitter.im/alexa-pi/Lobby)**  
- join our **[AlexaPi Users](https://plus.google.com/communities/105607055053826225738/)** user community on Google+  
