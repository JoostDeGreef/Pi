#!/usr/bin/python3
import RPi.GPIO as GPIO 

buttons = [8, 10]
state = [0, 0]

def print_state():
    print('\r {} {}   '.format(state[0],state[1]), end='', flush=True)

def button_callback(channel):
    i = buttons.index(channel)
    state[i] = 1 - state[i]
    print_state()
    # print("Button {0} state changed to {1}", channel, state)

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

GPIO.setup( 8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect( 8, GPIO.RISING, callback=button_callback, bouncetime=50)
GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback, bouncetime=50)

message = input("Press enter to quit\n\n")
GPIO.cleanup() # Clean up
