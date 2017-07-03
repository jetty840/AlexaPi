import time
from abc import ABCMeta
import logging
import socket
import os

from .baseplatform import BasePlatform

logger = logging.getLogger(__name__)

GPIO = None


class RPiLikePlatform(BasePlatform):
	__metaclass__ = ABCMeta

	def __init__(self, config, platform_name, p_GPIO):

		global GPIO
		GPIO = p_GPIO

		super(RPiLikePlatform, self).__init__(config, platform_name)

		self.button_pressed = False
		self.microphone_active = True

	def setup(self):
		GPIO.setup(self._pconfig['button'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self._pconfig['rec_light'], GPIO.OUT)
		GPIO.setup(self._pconfig['plb_light'], GPIO.OUT)
		GPIO.setup(self._pconfig['mute_light'], GPIO.OUT)
		GPIO.output(self._pconfig['rec_light'], GPIO.LOW)
		GPIO.output(self._pconfig['plb_light'], GPIO.LOW)
		GPIO.setup(self._pconfig['mute_light'], GPIO.LOW)
		self.neopixelChange('alexapi_startup')

	def neopixelChange(self, aname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
		s.connect(('127.0.0.1', self._pconfig['neopixel_udp_port']))
		s.send(aname)
		s.close()

	def is_microphone_on(self):
		return self.microphone_active

	def toggle_microphone_onoff(self):
		self.microphone_active = self.microphone_active ^ True
		logger.debug(self.microphone_active)
		logger.debug(self._pconfig['mute_light_invert'])
		if self.microphone_active:
			if self._pconfig['mute_light_invert'] == 1:
				gpioOut = GPIO.LOW
			else:
				gpioOut = GPIO.HIGH
		else:
			if self._pconfig['mute_light_invert'] == 1:
				gpioOut = GPIO.HIGH
			else:
				gpioOut = GPIO.LOW
		logger.debug(gpioOut)
		GPIO.output(self._pconfig['mute_light'], gpioOut)

	def indicate_failure(self):
		for _ in range(0, 5):
			time.sleep(.1)
			self.neopixelChange('alexapi_failure')
			GPIO.output(self._pconfig['rec_light'], GPIO.HIGH)
			time.sleep(.1)
			self.neopixelChange('alexapi_clear')
			GPIO.output(self._pconfig['rec_light'], GPIO.LOW)

	def indicate_success(self):
		for _ in range(0, 5):
			time.sleep(.1)
			self.neopixelChange('alexapi_success')
			GPIO.output(self._pconfig['plb_light'], GPIO.HIGH)
			time.sleep(.1)
			self.neopixelChange('alexapi_clear')
			GPIO.output(self._pconfig['plb_light'], GPIO.LOW)

	def after_setup(self, trigger_callback=None):

		self._trigger_callback = trigger_callback

		if self._trigger_callback:
			# threaded detection of button press
			GPIO.add_event_detect(self._pconfig['button'], GPIO.FALLING, callback=self.detect_button, bouncetime=100)

	def indicate_recording(self, state=True):
		self.neopixelChange('alexapi_recording' if state else 'alexapi_fadetoclear')
		GPIO.output(self._pconfig['rec_light'], GPIO.HIGH if state else GPIO.LOW)

	def indicate_playback(self, state=True):
		self.neopixelChange('alexapi_play' if state else 'alexapi_fadetoclear')
		GPIO.output(self._pconfig['plb_light'], GPIO.HIGH if state else GPIO.LOW)

	def indicate_processing(self, state=True):
		self.neopixelChange('alexapi_processing' if state else 'alexapi_fadetoclear')
		GPIO.output(self._pconfig['plb_light'], GPIO.HIGH if state else GPIO.LOW)
		GPIO.output(self._pconfig['rec_light'], GPIO.HIGH if state else GPIO.LOW)

	def detect_button(self, channel=None): # pylint: disable=unused-argument
		# time.sleep(.5)  # time for the button input to settle down

		if GPIO.input(self._pconfig['button']) == 0:
			self.button_pressed = True

			self._trigger_callback(self.force_recording)

			logger.debug("Button pressed!")
	
			rebootflag = False
			time_start = time.time()
			while GPIO.input(self._pconfig['button']) == 0:
				if ( time.time() - time_start ) >= 5:
					rebootflag = True	
				if rebootflag:
					 self.toggle_microphone_onoff()
				time.sleep(.1)

			if rebootflag:
				os.system('sudo /sbin/reboot')
				logger.debug("Reboot")

			logger.debug("Button released.")

			self.button_pressed = False

			time.sleep(.5)  # more time for the button to settle down

	# def wait_for_trigger(self):
	# 	# we wait for the button to be pressed
	# 	GPIO.wait_for_edge(self._pconfig['button'], GPIO.FALLING)

	def force_recording(self):
		return self.button_pressed

	def cleanup(self):
		GPIO.remove_event_detect(self._pconfig['button'])

		self.neopixelChange('alexapi_fadetoclear')
		GPIO.output(self._pconfig['rec_light'], GPIO.LOW)
		GPIO.output(self._pconfig['plb_light'], GPIO.LOW)
