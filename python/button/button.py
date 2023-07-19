#!/usr/bin/python3
import RPi.GPIO as GPIO 

buttons = [14, 15]
state = [0, 0]

def print_state():
    print('\r {} {}   '.format(state[0],state[1]), end='', flush=True)

def button_callback(channel):
    i = buttons.index(channel)
    state[i] = 1 - state[i]
    print_state()
    # print("Button {0} state changed to {1}", channel, state)
    GPIO.output(18, state[0])

GPIO.setwarnings(True)
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.OUT)

GPIO.add_event_detect(14, GPIO.RISING, callback=button_callback, bouncetime=50)
GPIO.add_event_detect(15, GPIO.RISING, callback=button_callback, bouncetime=50)

message = input("Press enter to quit\n\n")
GPIO.cleanup() # Clean up
