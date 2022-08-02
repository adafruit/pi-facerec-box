"""
Raspberry Pi Face Recognition Box Servo Calibration Sketch
Copyright 2013 Tony DiCola
"""

import RPi.GPIO as GPIO
import config

# pylint: disable=no-member

print("Servo Calibration")
print()
print("Use this tool to find servo pulse width values which move the")
print("lock latch to the locked and unlocked positions. Update config.py")
print("with the locked and unlocked servo pulsewidth values.")
print()
print("Most servos accept a range from 1000 to 2000 (in microseconds) with")
print("a center position around 1500. Some swing a bit wider, so you can")
print("try values 500 to 2500 if needed.")
print()
print("Press CTRL-C to quit")
print()

GPIO.setmode(GPIO.BCM)
GPIO.setup(config.LOCK_SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(config.LOCK_SERVO_PIN, 50)
servo.start(1500 / 200)  # Center servo timing

while True:
    val = input("Enter servo pulsewidth (500 to 2500), CTRL+C to quit:")
    try:
        val = int(val)
        if 500 <= val <= 2500:
            servo.ChangeDutyCycle(val / 200)
        else:
            raise ValueError
    except ValueError:
        print("Invalid value, must be between 500 and 2500!")
