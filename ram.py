class RAM(object):

    def __init__(self):
        self.__memory__ = (64 * 1024) * [0]
        self.name = "RAM"

    def __str__(self):
        return("This is the RAM object")
        
    def read(self, address):
        val = self.__memory__[address]
        return(val)
        
    def write(self, address, value):
        value = value & 0xFFFF
        self.__memory__[address] = value
               
    def clear_ram(self):
        self.__memory__[:] = len(self.__memory__) * [0]
    
        
        
