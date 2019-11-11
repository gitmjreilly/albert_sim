#!/usr/bin/python

from word_utilities import within_16_bits_check

class AddressSpace(object):

    # Formally define the amount of memory we support
    MEMORY_SIZE = 64 * 1024

    # We support 3 access categories for all 
    # memory in the simulator.
    # (The actual h/w supports NONE of this.
    # We can detect all memory access violations here (in this class)
    # since all memory i/o goes through.
    CODE_RO = 0
    DATA_RW = 1
    NO_ACCESS = 2

    def __init__(self):
        print "Initializing AddressSpace"
        self.device_list = []
        self.type_buffer = [AddressSpace.NO_ACCESS] * AddressSpace.MEMORY_SIZE
        self.is_fatal_memory_error = False
        self.is_memory_protection_on = False

    def __str__(self):
        return("No string representation")
        

    def add_device(self, base_address, max_address, device):
        if (base_address < 0) :
            print("FATAL - tried to add device below address 0")
            print("device [%s]" % (device))
        if (max_address > (self.MEMORY_SIZE - 1)) :
            print("FATAL - tried to add device above MEMORY_SIZE")
            print("device [%s]" % (device))
           
        device_description  = dict()
        device_description["base_address"] = base_address
        device_description["max_address"] =  max_address
        device_description["device"] = device
        self.device_list.append(device_description)

        
    def super_read(self, absolute_address):
        device_is_found = 0
        for memory_mapped_device in self.device_list:
            base_address = memory_mapped_device['base_address']
            max_address = memory_mapped_device['max_address']
            if ( (absolute_address >= base_address) and (absolute_address <= max_address) ) :
                relative_address = absolute_address - base_address
                value = memory_mapped_device['device'].read(relative_address)
                within_16_bits_check(value)
                return(value, self.type_buffer[absolute_address])
        
        s = "FATAL Sim error in address_space.super_read() addr [%08X] No device mapped to this address" % (absolute_address)
        e = BaseException(s)
        raise(e)

        
  
    def read(self, absolute_address):
        if (self.is_memory_protection_on) :
            if (self.type_buffer[absolute_address] != AddressSpace.DATA_RW):
                print "FATAL Error!  Tried to read from addr %08X but type is NOT DATA_RW." % \
                    absolute_address
                self.is_fatal_memory_error = True
                return(0)

        if (absolute_address > (self.MEMORY_SIZE - 1)):
            s = "FATAL Sim error in address_space.read() addr [%08X] > max mem addr [%08X]" % (absolute_address, (self.MEMORY_SIZE - 1))
            e = BaseException(s)
            raise(e)

        if (absolute_address < 0):
            s = "FATAL Sim error in address_space.read() addr [%08X] < 0" % (absolute_address)
            e = BaseException(s)
            raise(e)
        device_is_found = 0
        for memory_mapped_device in self.device_list:
            base_address = memory_mapped_device['base_address']
            max_address = memory_mapped_device['max_address']
            if ( (absolute_address >= base_address) and (absolute_address <= max_address) ) :
                relative_address = absolute_address - base_address

                value = memory_mapped_device['device'].read(relative_address)
                within_16_bits_check(value)
                return(value)

        
        s = "FATAL Sim error in address_space.read() addr [%08X] No device mapped to this address" % (absolute_address)
        e = BaseException(s)
        raise(e)
            

        
    def code_read(self, absolute_address):
        if (self.is_memory_protection_on) :
            if (self.type_buffer[absolute_address] != AddressSpace.CODE_RO):
                print "FATAL Error!  Tried to read CODE from addr %08X but type is NOT CODE_RO." % \
                    absolute_address
                self.is_fatal_memory_error = True
                return(0)

        if (absolute_address > (self.MEMORY_SIZE - 1)):
            s = "FATAL Sim error in address_space.code_read() addr [%08X] > max mem addr [%08X]" % (absolute_address, (self.MEMORY_SIZE - 1))
            e = BaseException(s)
            raise(e)

            
        if (absolute_address < 0):
            s = "FATAL Sim error in address_space.code_read() addr [%08X] < 0" % (absolute_address)
            e = BaseException(s)
            raise(e)
        device_is_found = 0
        for memory_mapped_device in self.device_list:
            base_address = memory_mapped_device['base_address']
            max_address = memory_mapped_device['max_address']
            if ( (absolute_address >= base_address) and (absolute_address <= max_address) ) :
                relative_address = absolute_address - base_address

                value = memory_mapped_device['device'].read(relative_address)
                within_16_bits_check(value)
                return(value)

        s = "FATAL Sim error in address_space.code_read() addr [%08X] No device mapped to this address" % (absolute_address)
        e = BaseException(s)
        raise(e)
        


        
    def write(self, absolute_address, value):    

        within_16_bits_check(value)

        if (self.is_memory_protection_on) :
            if (self.type_buffer[absolute_address] != AddressSpace.DATA_RW):
                print "FATAL Error!  Tried to write to addr %08X but type is not data." % \
                    absolute_address
                self.is_fatal_memory_error = True
                return(0)

        if (absolute_address > (self.MEMORY_SIZE - 1)):
            s = "FATAL Sim error in address_space.write() addr [%08X] > max mem addr [%08X]" % (absolute_address, (self.MEMORY_SIZE - 1))
            e = BaseException(s)
            raise(e)

            
        if (absolute_address < 0):
            s = "FATAL Sim error in address_space.write() addr [%08X] < 0" % (absolute_address)
            e = BaseException(s)
            raise(e)

            
        if (value != (value & 0xFFFF)):
            s = "ERROR tried to WRITE to value outside 16 bit range (decimal) [%d] " % (value)
            e = BaseException(s)
            raise(e)
        device_is_found = 0
        for memory_mapped_device in self.device_list:
            base_address = memory_mapped_device['base_address']
            max_address = memory_mapped_device['max_address']
            if ( (absolute_address >= base_address) and (absolute_address <= max_address) ) :
                relative_address = absolute_address - base_address
                memory_mapped_device['device'].write(relative_address, value)
                return
        
        s = "FATAL Sim error in address_space.write() addr [%08X] No device mapped to this address" % (absolute_address)
        e = BaseException(s)
        raise(e)

        
    def write_type(self, absolute_address, value):    
        self.type_buffer[absolute_address] = value
        
    def set_memory_protection_flag(self, state):
        self.is_memory_protection_on = state
        



class TestMemMappedDevice(object):

    def __init__(self):
        self.__mem__ = [0] * 50
        
    def __str__(self):
        return("no string rep for this class")
        
    def read(self, address):
        print("Reading from address %x" % address)
        return(self.__mem__[address])
        
    def write(self, address, value):
        self.__mem__[address] = value
        print("writing val %x to addr %x" % (value, address) )
        
  



#
# Main test function
def main():
    print "testing AddressSpace..."
    test_device_1 = TestMemMappedDevice()
    A = AddressSpace()
    A.add_device(100, 149, test_device_1)
    A.write(101, 17)
    A.write(102, 0xFFFF)
    A.write(103, -1)
    print(str(A.read(101)))


    
if (__name__ == "__main__"):
    main()
