
class Register(object):

    def __init__(self):
        """ Initialize with the value """
        self.value = 0

    def __str__(self):
        return(str(self.value))
        
    def read(self):
        return(self.value)
        
    def write(self, value):
        self.value = value & 0xFFFF
        
    def inc(self):
        self.value = (self.value + 1) & 0xFFFF;


    def dec(self):
        self.value = (self.value - 1) & 0xFFFF;

class Register_With_History(object):
    NUM_HISTORY_ENTRIES = 1000

    def __init__(self):
        """ Initialize with the value """
        self.value = 0
        self.history = Register_With_History.NUM_HISTORY_ENTRIES * [0]
        # _head is a pointer at the last entry NOT the next free spot
        # There is no TAIL; this is a circular buffer
        self._head = 0

    def __str__(self):
        return(str(self.value))
        
    def read(self):
        value = self.value
        if (value != (value & 0xFFFF)):
            print("ERROR tried to read to value outside 16 bit range [%08X] to register " % (value))
            return(0)
            
        return(self.value)
        

        
    def write(self, value):
        if (value != (value & 0xFFFF)):
            print("ERROR tried to write to value outside 16 bit range [%08X] to register " % (value))
            return(0)
            
        self.history[self._head] = self.value
        self._head = self._head + 1
        if (self._head == Register_With_History.NUM_HISTORY_ENTRIES):
            self._head = 0
        self.value = value & 0xFFFF
        
    def inc(self):
        value = self.value
        if (value != (value & 0xFFFF)):
            print("ERROR tried to read to increment value outside 16 bit range [%08X] to register " % (value))
            return(0)
            
        self.write((self.value + 1) & 0xFFFF)


    def dec(self):
        value = self.value
        if (value != (value & 0xFFFF)):
            print("ERROR tried to read to decrement value outside 16 bit range [%08X] to register " % (value))
            return(0)
            
        self.write((self.value - 1) & 0xFFFF)
        
print " Just imported register. "        
