

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
class State(object):
    __metaclass__ = Singleton

    pump = [0]
    valves = [0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        print("State initializing")

    def _executeCmd(self, object, index, cmd):
        if cmd > 1:
            object[index] = 1 - object[index]
        else:
            object[index] = cmd

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

