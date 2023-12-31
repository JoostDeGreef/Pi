import RPi.GPIO as GPIO

from time import sleep

class Hardware(object):

    pump =    [23]
    sensor =  [18]
    valves =  [19, 20, 21, 22, 24, 25, 26, 27]

    buttons = [ 2,  3,  4,  5,  6,  7,  8,  9]
    leds =    [10, 11, 12, 13, 14, 15, 16, 17]
    
    callbacks = [None, None, None, None, None, None, None, None]

    def __init__(self):
        print("Hardware initializing")
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        print("Configuring pump on GPIO {0}".format(self.pump[0]))
        GPIO.setup(self.pump[0], GPIO.OUT)
        for valve in self.valves:
            print("Configuring valve on GPIO {0}".format(valve))
            GPIO.setup(valve, GPIO.OUT, initial=GPIO.HIGH)
        for button in self.buttons:
            print("Configuring button on GPIO {0}".format(button))
            if button == 2 or button == 3:
                GPIO.setup(button, GPIO.IN)
            else:
                GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            #GPIO.add_event_detect(button, GPIO.RISING, callback=self._buttonCallback, bouncetime=300)   
            #GPIO.add_event_detect(button, GPIO.FALLING, callback=self._buttonCallback, bouncetime=300)
            GPIO.add_event_detect(button, GPIO.FALLING, callback=self._buttonCallback)
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
        # GPIO.output(self.leds, status) 
        for i in range(0, len(self.valves)):
            if status[i] == 0:
                GPIO.output(self.valves[i], GPIO.HIGH)
                GPIO.output(self.leds[i], GPIO.LOW)
            else:
                GPIO.output(self.valves[i], GPIO.LOW)
                GPIO.output(self.leds[i], GPIO.HIGH)
        state =  [0, 0, 0, 0, 0, 0, 0, 0]
        mismatch = 0
        for i in range(0, len(self.valves)):
            state[i] = 1 - GPIO.input(self.valves[i]);
            if state[i] != status[i]:
                mismatch = mismatch + 1;
        if mismatch > 0:
            print("Set valves to: {0} {1} {2} {3} {4} {5} {6} {7}".format(status[0],status[1],status[2],status[3],status[4],status[5],status[6],status[7]))
            print(" Actual state: {0} {1} {2} {3} {4} {5} {6} {7} -> retrying".format(state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7]))
            self.setValues(status)
        else:
            for i in range(0, len(self.valves)):
                state[i] = GPIO.input(self.leds[i]);
                if state[i] != status[i]:
                    mismatch = mismatch + 1;
            if mismatch > 0:
                print("Set valves to: {0} {1} {2} {3} {4} {5} {6} {7}".format(status[0],status[1],status[2],status[3],status[4],status[5],status[6],status[7]))
                print("    Led state: {0} {1} {2} {3} {4} {5} {6} {7} -> retrying".format(state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7]))
                self.setValues(status)
        
    def _buttonCallback(self, channel):
        i = self.buttons.index(channel)
        sleep(0.05) # debounce in GPIO fails sometimes
        if GPIO.input(channel) == 0:
            print("(hardware) Button {0} callback".format(i))
            if self.callbacks[i]:
                self.callbacks[i](i)
            # actively wait untill button is released
            count = 0
            while count < 3:
                sleep(0.05)
                count = count + 1
                if GPIO.input(channel) == 0:
                    count = 0
                
        

