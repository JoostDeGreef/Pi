from hardware import Hardware

class State(object):

    pump = [0]
    valves = [0, 0, 0, 0, 0, 0, 0, 0]
    hardware = Hardware()
    
    def __init__(self):
        print("State initializing")
        self._updateHardware()
        for i in range(0, 8):
            self.hardware.registerButton(i, self._buttonCallback)

    def _buttonCallback(self, button):
        #print("(state) Button {0} callback".format(button))
        self.setValue(button+1,2);

    def _executeCmd(self, object, index, cmd):
        if cmd > 1:
            object[index] = 1 - object[index]
        else:
            object[index] = cmd
            
    def _updateHardware(self):
        self.hardware.setPump(self.pump[0])
        self.hardware.setValves(self.valves)

    def setValue(self, valve, cmd):
        # cmd 0, 1, 2
        if valve == 0:
            self._executeCmd(self.pump, 0, cmd)
            if self.pump[0] == 0:
                for i in range(0, len(self.valves)):
                    self._executeCmd(self.valves, i, 0)
        else:
            self._executeCmd(self.valves, valve-1, cmd)
            s = sum(self.valves)
            if s == 0:
                self._executeCmd(self.pump, 0, 0)
            else:
                self._executeCmd(self.pump, 0, 1)
        self._updateHardware()
        
    def getValves(self):
        return "".join(str(v) for v in self.valves)
    
    def getPump(self):
        return str(self.pump[0])
    
    def getStatus(self):
        v = sum(self.valves)
        p = sum(self.pump)
        if p == 0:
            if v > 0:
                return "Valve open, but pump not running"
            return "Pump not running"
        else:
            if v == 0:
                return "Pump running, but no valves open"
            elif v == 1:
                return "Pump running, 1 valve open"
            elif v > 2:
                return "Pump running, " + str(v) + " valves open (too many!)"
            return "Pump running, " + str(v) + " valves open"

