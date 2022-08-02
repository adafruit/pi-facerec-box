"""
Raspberry Pi Face Recognition Treasure Box
Treasure Box Class
Copyright 2013 Tony DiCola
"""

import time
import RPi.GPIO as GPIO
import config

# pylint: disable=no-member


class Box:
    """Class to represent the state and encapsulate access to the hardware of
    the treasure box."""

    def __init__(self):
        # Initialize lock servo and button.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.LOCK_SERVO_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(config.LOCK_SERVO_PIN, 50)
        self.servo.start(config.LOCK_SERVO_LOCKED / 200)  # Locked position
        GPIO.setup(config.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Set initial box state.
        self.button_state = GPIO.input(config.BUTTON_PIN)
        self.is_locked = None

    def lock(self):
        """Lock the box."""
        # Original code used RPIO (now deprecated), which used microsecond
        # PWM timing. RPi.GPIO PWM expects duty cycle (0.0 to 100.0), so
        # divide usec by 200 (because 50 Hz PWM for servo) so we can keep the
        # same units/config as original code and not break existing installs.
        self.servo.ChangeDutyCycle(config.LOCK_SERVO_LOCKED / 200)
        self.is_locked = True

    def unlock(self):
        """Unlock the box."""
        self.servo.ChangeDutyCycle(config.LOCK_SERVO_UNLOCKED / 200)
        self.is_locked = False

    def is_button_up(self):
        """Return True when the box button is pressed."""
        old_state = self.button_state
        self.button_state = GPIO.input(config.BUTTON_PIN)
        # Check if transition from down to up
        if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
            # Wait 20 milliseconds and measure again to debounce switch.
            time.sleep(20.0 / 1000.0)
            self.button_state = GPIO.input(config.BUTTON_PIN)
            if self.button_state == config.BUTTON_UP:
                return True
        return False
