import RPi.GPIO as GPIO

class Hardware(object):

    pump =    [23]
    sensor =  [18]
    valves =  [24, 25,  8,  7, 12, 16, 20, 21]

    buttons = [26,  4, 27, 22,  9, 11,  5, 13]
    leds =    [ 2, 14, 15, 17, 10,  6,  3, 19]
    
    callbacks = [None, None, None, None, None, None, None, None]

    def __init__(self):
        print("Hardware initializing")
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        print("Configuring pump on GPIO {0}".format(self.pump[0]))
        GPIO.setup(self.pump[0], GPIO.OUT)
        for valve in self.valves:
            print("Configuring valve on GPIO {0}".format(valve))
            GPIO.setup(valve, GPIO.OUT)
        for button in self.buttons:
            print("Configuring button on GPIO {0}".format(button))
            GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(button, GPIO.RISING, callback=self._buttonCallback, bouncetime=70)   
        for led in self.leds:
            print("Configuring led on GPIO {0}".format(led))
            GPIO.setup(led, GPIO.OUT)

    def registerButton(self, button, callback):
        self.callbacks[button] = callback

    def setPump(self, status):
        if status == 0:
            GPIO.output(self.pump[0], GPIO.LOW)
        else:
            GPIO.output(self.pump[0], GPIO.HIGH)
            
    def setValves(self, status):
        for i in range(0, len(self.valves)):
            if status[i] == 0:
                GPIO.output(self.valves[i], GPIO.LOW)
                GPIO.output(self.leds[i], GPIO.LOW)
            else:
                GPIO.output(self.valves[i], GPIO.HIGH)
                GPIO.output(self.leds[i], GPIO.HIGH)
            
    def _buttonCallback(self, channel):
        i = self.buttons.index(channel)
        #print("(hardware) Button {0} callback".format(i))
        if self.callbacks[i]:
            self.callbacks[i](i)
        
        

