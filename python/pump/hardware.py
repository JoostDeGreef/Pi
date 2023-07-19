import RPi.GPIO as GPIO

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class Hardware(object):
    __metaclass__ = Singleton

    pump = [11]
    sensor = [18]
    valves = [16, 20, 21, 5, 6, 13, 19, 26]
    buttons = [14, 15, 23, 24, 25, 8, 7, 12]
    leds = [2, 3, 4, 17, 27, 22, 10, 9]

    def __init__(self):
        print("Hardware initializing")
        GPIO.setwarnings(True)
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pump[0], GPIO.OUT)
        for valve in valves:
            GPIO.setup(valve, GPIO.OUT)
        for button in buttons:
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(button, GPIO.RISING, callback=button_callback, bouncetime=70)
        for led in leds:
            GPIO.setup(led, GPIO.OUT)

    def button_callback(channel):
        i = buttons.index(channel)
        print("Button {0} callback", i)

#message = input("Press enter to quit\n\n")
#GPIO.cleanup() # Clean up
