""" Jamet's CPU Class """

from register import Register, Register_With_History

# TODO - figure out where to put opcode_to_mnemonic
# General stuff to initialize a map used for disassembly

opcode_to_mnemonic = dict()
opcode_to_mnemonic[2] = "DO_LIT"
opcode_to_mnemonic[3] = "HALT"
opcode_to_mnemonic[4] = "BRA"
opcode_to_mnemonic[5] = "LESS"
opcode_to_mnemonic[6] = "++"
opcode_to_mnemonic[7] = "DROP"
opcode_to_mnemonic[8] = "STORE"
opcode_to_mnemonic[9] = "FETCH"
opcode_to_mnemonic[10] = "JSR"
opcode_to_mnemonic[11] = "RET"
opcode_to_mnemonic[12] = "JMPF"
opcode_to_mnemonic[13] = "TO_R"
opcode_to_mnemonic[14] = "FROM_R"
opcode_to_mnemonic[16] = "RP_FETCH"
opcode_to_mnemonic[17] = "RP_STORE"
opcode_to_mnemonic[18] = "R_FETCH"
opcode_to_mnemonic[19] = "DUMP"
opcode_to_mnemonic[20] = "SP_FETCH"
opcode_to_mnemonic[21] = "SWAP"
opcode_to_mnemonic[22] = "OVER"
opcode_to_mnemonic[23] = "SP_FETCH"
opcode_to_mnemonic[24] = "+"
opcode_to_mnemonic[25] = "-"
opcode_to_mnemonic[26] = "NEG?"
opcode_to_mnemonic[27] = "AND"
opcode_to_mnemonic[28] = "OR"
opcode_to_mnemonic[29] = "XOR"
opcode_to_mnemonic[30] = "*"

opcode_to_mnemonic[31] = "EQUAL"
opcode_to_mnemonic[32] = "UM+"
opcode_to_mnemonic[52] = "STORE2"



######################################################################
def is16BitPositive(val) :

	if (val > 65535) :
		print "FATAL Error saw > 16 bit val in is16BitPositive!"
		sys.exit(1)
	

	if (val <= 32767) :
		return(1)
	else :
		return(0)
######################################################################

def special_write(self, value):
    self.value = value & 0xFFFF
    print "*** SPECIAL_WRITE ***"
 

class CPUStatus(object):
    def __init__(self, absolute_address, cs, ds, psp, rsp, opcode, disassembly_string):
        self.d = dict()
        self.d["ABSAddr"] = absolute_address
        self.d["CS"] = cs
        self.d["DS"] = ds
        self.d["PSP"] = psp
        self.d["RSP"] = rsp
        self.d["opcode"] = opcode
        self.d["disassembly_string"] = disassembly_string

#    def __str__(self):
#        tmp =  ""
#        tmp += "absaddr   : %08X | " % (self.d["ABSAddr"])
#        tmp += "CS   : %04X | " % (self.d["CS"])
#        tmp += "DS   : %04X | " % (self.d["DS"])
#        tmp += "PSP   : %04X | " % (self.d["PSP"])
#        tmp += "RSP   : %04X | " % (self.d["RSP"])
#        tmp += "opcode   : %04X | " % (self.d["opcode"])
#
#        mnemonic = opcode_to_mnemonic.get(self.d["opcode"], "TBD")
#        if (self.d["disassembly_string"] == ""):
#            tmp += mnemonic 
#        else:
#            tmp += self.d["disassembly_string"]
#        return(tmp)

    def __str__(self):
        tmp =  ""
        tmp += "@%08X | " % (self.d["ABSAddr"])
        tmp += "%04X | " % (self.d["opcode"])

        mnemonic = opcode_to_mnemonic.get(self.d["opcode"], "TBD")
        if (self.d["disassembly_string"] == ""):
            s = "%s |" % (mnemonic)
        else:
            s = "%s" % (self.d["disassembly_string"])

        l  = s.split('|')
        try:
            s2 = "%-30s | %-70s |" % (l[0], l[1])
        except:
            s2 = s
        tmp += s2


        # tmp += "CS   : %04X | " % (self.d["CS"])
        # tmp += "DS   : %04X | " % (self.d["DS"])
        tmp += "PSP   : %04X | " % (self.d["PSP"])
        tmp += "RSP   : %04X | " % (self.d["RSP"])

        return(tmp)





    def add_disassembly_string(self, disassembly_string):
        self.d["disassembly_string"] = disassembly_string

 
class CPU(object):

    AND_OPC = 27
    BRANCH_OPC = 4
    BRANCH_FALSE_OPC = 12
    CS_FETCH_OPC = 43
    DI_OPC = 37
    DS_FETCH_OPC = 42
    DO_LIT_OPC = 2
    DROP_OPC = 7
    DUP_OPC = 19
    EI_OPC = 35
    EQUAL_OPC = 31
    ES_FETCH_OPC = 41
    FETCH_OPC = 9
    FROM_R_OPC = 14
    HALT_OPC = 3
    JSR_OPC = 10
    JSR_INT_OPC = 33
    K_SP_STORE_OPC = 47
    LESS_OPC = 5
    LONG_FETCH_OPC = 44
    LONG_STORE_OPC = 45
    # For use on simulator only.
    LONG_TYPE_STORE_OPC = 53
    L_VAR_OPC = 51
    MUL_OPC = 30
    NEG_OPC = 26
    NOP_OPC = 1
    OR_OPC = 28
    OVER_OPC = 22
    PLUS_OPC = 24
    PLUS_PLUS_OPC = 6
    POPF_OPC = 49
    PUSHF_OPC = 48
    R_FETCH_OPC = 18
    RET_OPC = 11
    RETI_OPC = 34
    RP_FETCH_OPC = 16
    RP_STORE_OPC = 17
    S_LESS_OPC = 50
    SLL_OPC = 15
    SP_FETCH_OPC = 20
    SP_STORE_OPC = 23
    SRA_OPC = 36
    SRL_OPC = 38
    STORE_OPC = 8
    STORE2_OPC = 52
    SUB_OPC = 25
    SWAP_OPC = 21
    SYSCALL_OPC = 46
    TO_DS_OPC = 40
    TO_ES_OPC = 39
    TO_R_OPC = 13
    UM_PLUS_OPC = 32
    XOR_OPC = 29

    def special_write(self, value):
        print "*** SPECIAL_WRITE ***"
        print "    CS:PC %4X:%4XX    old value : %4X new value : %4X" % (self.CS.value, self.PC.value,  self.INT_CTL_LOW.value, value)
        self.INT_CTL_LOW.value = value & 0xFFFF
    

    def __init__(self):
        """ Initialize with the base_type """
        self.PC = Register_With_History()
        
        self.DS = Register()
        self.CS = Register()
        self.ES = Register()
        
        self.PTOS = Register()
        self.RTOS = Register()

        self.PSP = Register()
        self.PSP.write(0xFF00)
        
        self.RSP = Register()
        self.RSP.write(0xFE00)

        self.INT_CTL_LOW = Register()
        # self.INT_CTL_LOW.write = self.special_write

        self._interrupt_pin = 0
        
        self._address_history = 10000 * [0x0000]
        
        self._break_point_list = dict()
        self._prev_break_point_address = 0x00000

        
        # set_opcodes()
        print "CPU has been initialized..."

    def set_memory_methods(self, 
        mem_read_method, 
        mem_write_method, 
        code_read_method, 
        mem_write_type):
        
        self.mem_read  = mem_read_method
        self.mem_write = mem_write_method
        self.code_read = code_read_method
        self.mem_write_type = mem_write_type
        
    def __str__(self):
        tmp =  "  No self here.\n"
        tmp = "CPU State : \n"
        tmp += "PC   : %04X  \n" % (self.PC.read() )
        tmp += "PTOS : %04X  RTOS: %04X\n" % (self.PTOS.read(), self.RTOS.read())
        tmp += "CS   : %04X  DS  : %04X ES   : %04X \n" % (self.CS.read(), self.DS.read(), self.ES.read())
        tmp += "PSP  : %04X  RSP : %04X \n" % (self.PSP.read(), self.RSP.read())
        tmp += "INT_CTL_LOW   : %04X \n" %self.INT_CTL_LOW.read()
        tmp += "Interrupt State : %d\n" % self._interrupt_pin
        return(tmp)
  
    def set_pc(self, val):
        self.PC.write(val)
       
    def set_break_point(self) :

        def cmp(a, b):
            if (a < b):
                return(-1)
            elif (a > b):
                return(1)
            else:
                return(0)
        
        
        s = raw_input("Enter PC (in hex) for breakpoint>")
        try:
            absolute_address = int(s.upper(), 16)    
        except:
            return
        
        self._break_point_list[absolute_address] = 1
        
        self._break_point_list.keys().sort(cmp)
 

    def clear_break_point(self) :
        
        PC = raw_input("Enter PC (in hex) for breakpoint>")
        try:
            PC = int(PC.upper(), 16)    
        except:
            return
        
        absolute_address  = PC

        if (self._break_point_list.has_key(absolute_address) ) :
            del(self._break_point_list[absolute_address])
        

    def clear_all_break_points(self) :
        self._break_point_list = dict()


    def show_break_points(self) :       
        for break_point in (self._break_point_list.keys()) :
            print "   %04X" % break_point

    def show_address_history(self):
        print "Address history : "
        for history_record in (self._address_history):
            print history_record

    def clear_address_history(self):
        self._address_history = 10000 * [0x0000]


    def step(self):
        absolute_address = (self.CS.read() << 4) + self.PC.read()     

        if ((self._interrupt_pin == 1) and ((self.INT_CTL_LOW.read() & 0x0001) == 1)):
            # We have NOT incremented the PC.  JSR_INT assumes it points at the 
            # instruction to execute when RETI is executed.
            status = self._do_instruction(CPU.JSR_INT_OPC, absolute_address)
        else:
            if (self._break_point_list.has_key(absolute_address) ) :
                if (self._prev_break_point_address != absolute_address):                
                    print "CPU encountered breakpoint at %08X" % (absolute_address)
                    self._prev_break_point_address = absolute_address
                    return(1)


            # Notice we use "code_read" here.  In this way, the simulator
            # can confirm that only code is being executed
            opcode = self.code_read(absolute_address)

        
            
            # Please note; all of the instructions assume the PC is pointing
            # at the location AFTER the current opcode
            self.PC.inc()
            status = self._do_instruction(opcode, absolute_address)
        return(status)
        
        
    def _do_instruction(self, opcode, absolute_address):
        # PC is assumed to point at the mem location after
        # the location where this opcode is stored.
        #
        # absolute_address is the address where this opcode was found
        # We have to pass it in because the PC already points to the location AFTER the opcode

        # This is the only place where we actually run an instruction.
        # So this is where the address history can be captured AND
        # it is the only place where we should act on break points

        if (len(self._address_history) > 100000) :
            self._address_history = self._address_history[50000:]


        AND_OPC = 27
        BRANCH_OPC = 4
        BRANCH_FALSE_OPC = 12
        CS_FETCH_OPC = 43
        DI_OPC = 37
        DS_FETCH_OPC = 42
        DO_LIT_OPC = 2
        DROP_OPC = 7
        DUP_OPC = 19
        EI_OPC = 35
        EQUAL_OPC = 31
        ES_FETCH_OPC = 41
        FETCH_OPC = 9
        FROM_R_OPC = 14
        HALT_OPC = 3
        JSR_OPC = 10
        JSR_INT_OPC = 33
        K_SP_STORE_OPC = 47
        LESS_OPC = 5
        LONG_FETCH_OPC = 44
        LONG_STORE_OPC = 45
        # For use on simulator only.
        LONG_TYPE_STORE_OPC = 53
        L_VAR_OPC = 51
        MUL_OPC = 30
        NEG_OPC = 26
        NOP_OPC = 1
        OR_OPC = 28
        OVER_OPC = 22
        PLUS_OPC = 24
        PLUS_PLUS_OPC = 6
        POPF_OPC = 49
        PUSHF_OPC = 48
        R_FETCH_OPC = 18
        RET_OPC = 11
        RETI_OPC = 34
        RP_FETCH_OPC = 16
        RP_STORE_OPC = 17
        S_LESS_OPC = 50
        SLL_OPC = 15
        SP_FETCH_OPC = 20
        SP_STORE_OPC = 23
        SRA_OPC = 36
        SRL_OPC = 38
        STORE_OPC = 8
        STORE2_OPC = 52
        SUB_OPC = 25
        SWAP_OPC = 21
        SYSCALL_OPC = 46
        TO_DS_OPC = 40
        TO_ES_OPC = 39
        TO_R_OPC = 13
        UM_PLUS_OPC = 32
        XOR_OPC = 29

        # print "DEBUG PC is %x" % self.PC.read()
    
        scaledCS = self.CS.read() << 4
        scaledDS = self.DS.read() << 4
        scaledES = self.ES.read() << 4

        stack_string = "PSTACK => "
        for i in range(3, 0, -1):
            stack_string += "%04X " % (self.mem_read(scaledDS + self.PSP.read() - i))
        stack_string += "PTOS:%04X" % (self.PTOS.read())

        stack_string += "   RSTACK => "
        for i in range(3, 0, -1):
            stack_string += "%04X " % (self.mem_read(scaledDS + self.RSP.read() - i))
        stack_string += "RTOS:%04X" % (self.RTOS.read())


        left_operand = self.mem_read(scaledDS + self.PSP.read() - 1)
        right_operand = self.PTOS.read()
        inline_operand = self.code_read(self.PC.read() + scaledCS)
        rtos_operand = self.RTOS.read()
        psp_operand = self.PSP.read()
        rsp_operand = self.RSP.read()


        
        # This is the return status for this method
        # default is 0 which means OK
        return_status = 0

        # Create a default history entry 
        # We'll append this to history unless a specific history entry is created
        # when an instruction is handled.
        c = CPUStatus(absolute_address, 
            self.CS.read(), self.DS.read(), self.PSP.read(), 
            self.RSP.read(), opcode, "")

        if (opcode == AND_OPC):

            disassembly_string = "[%04X %04X] AND | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)


            self.PSP.dec()
            self.PTOS.write(self.PTOS.read() & self.mem_read(scaledDS + self.PSP.read()))
            return(return_status)
        

        if (opcode == BRANCH_OPC):
            disassembly_string = "BRA %04X | %s" % (inline_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PC.write(self.code_read(self.PC.read() + scaledCS))
            return(return_status)
        

        if (opcode == BRANCH_FALSE_OPC):
            disassembly_string = "[%04X] JMPF %04X | %s" % (right_operand, inline_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            if (self.PTOS.read() == 0):
                # Consume the boolean and update PTOS
                self.PSP.dec()
                literal = self.mem_read(scaledDS + self.PSP.read())
                self.PTOS.write(literal)
                self.PC.write(self.code_read(self.PC.read() + scaledCS))
                return(return_status)
            
            else:
                self.PSP.dec()
                literal = self.mem_read(scaledDS + self.PSP.read())
                self.PTOS.write(literal)
                self.PC.inc()
                return(return_status)
            
        

        if (opcode == CS_FETCH_OPC):
            disassembly_string = "CS_FETCH" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)





            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()
            self.PTOS.write(self.CS.read())
            return(return_status)
        

        if (opcode == DI_OPC):
            disassembly_string = "DI" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.INT_CTL_LOW.write(self.INT_CTL_LOW.read() & 0xFFFE)
            return(return_status)
        

        if (opcode == DO_LIT_OPC):
            disassembly_string = "DO_LIT %04X | %s" % (inline_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)


            # Write the self.PTOS To location where self.PSP points
            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()
            literal = self.code_read(scaledCS + self.PC.read())
            self.PTOS.write(literal)
            self.PC.inc()
            return(return_status)
        

        if (opcode == DROP_OPC):
            disassembly_string = "[%04X] DROP | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PSP.dec()
            literal = self.mem_read(scaledDS + self.PSP.read())
            self.PTOS.write(literal)
            return(return_status)
        

        if (opcode == DS_FETCH_OPC):
            disassembly_string = "DS_FETCH" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()
            self.PTOS.write(self.DS.read())
            return(return_status)
        

        if (opcode == DUP_OPC):
            disassembly_string = "[%04X] DUP | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()
            return(return_status)
        

        if (opcode == EI_OPC):
            disassembly_string = "EI" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.INT_CTL_LOW.write(self.INT_CTL_LOW.read() | 0x0001)
            return(return_status)
        


        if (opcode == EQUAL_OPC):


            disassembly_string = "[%04X %04X] EQUAL | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)


            self.PSP.dec()
            if (self.PTOS.read() == self.mem_read(self.PSP.read() + scaledDS)):
                self.PTOS.write(0xFFFF)
            
            else:
                self.PTOS.write(0x0000)
            
            return(return_status)
        

        if (opcode == ES_FETCH_OPC):
            disassembly_string = "ES_FETCH" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()
            self.PTOS.write(self.ES.read())
            return(return_status)
        

        if (opcode == FETCH_OPC):
            disassembly_string = "[%04X] FETCH | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)


            self.PTOS.write(self.mem_read(scaledDS + self.PTOS.read()))
            return(return_status)
        

        if (opcode == FROM_R_OPC):
            disassembly_string = "FROM_R (RTOS: %04X) | %s" % (rtos_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(self.PSP.read() + scaledDS , self.PTOS.read())
            self.PSP.inc()
            self.PTOS.write(self.RTOS.read())
            self.RSP.dec()
            self.RTOS.write(self.mem_read(self.RSP.read() + scaledDS))
            return(return_status)
        
        if (opcode == HALT_OPC):
            disassembly_string = "HALT | %s" % (stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            print "Saw halt instruction"
            return_status = 1
            return(return_status)

        
        if (opcode == JSR_OPC):

            disassembly_string = "JSR %04X | %s" % (inline_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(self.RSP.read() + scaledDS , self.RTOS.read())
            self.RSP.inc()
            self.RTOS.write(self.PC.read() + 1)
            self.PC.write(self.code_read(self.PC.read() + scaledCS))
            return(return_status)
        


        if (opcode == JSR_INT_OPC):
            self._address_history.append(c)

            H = self.RSP.read()

            self.mem_write(self.RSP.read() + scaledDS , self.DS.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.CS.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.ES.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.PSP.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.PTOS.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.PC.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.INT_CTL_LOW.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , H)

            self.RSP.inc()
            self.INT_CTL_LOW.write(self.INT_CTL_LOW.read() & 0xFFFE)

            self.PC.write(0xFD00)
            self.CS.write(0x0000)
            return(return_status)
          
        
        if (opcode == K_SP_STORE_OPC):
            self._address_history.append(c)

            self.DS.write(0x0000)
            self.PSP.write(self.PTOS.read())
            return(return_status)
        

        if (opcode == L_VAR_OPC):
            self._address_history.append(c)

            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()

            literal = self.code_read(scaledDS + self.PC.read())
            self.PTOS.write(literal + self.RTOS.read())
            self.PC.inc()

            return(return_status)
        

        if (opcode == LESS_OPC):

            disassembly_string = "[%04X %04X] LESS | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            # usage a b LESS
            self.PSP.dec()
            self.PTOS.read()
            a = self.mem_read(self.PSP.read() + scaledDS) 
            b = self.PTOS.read()


            self.PTOS.write(0)
            if ((is16BitPositive(a) and (is16BitPositive(b)))):
                if (a < b): 
                    self.PTOS.write(0xFFFF) 

                return(return_status) 
            
                
            if ((not is16BitPositive(a) and (is16BitPositive(b)))):
                self.PTOS.write(0xFFFF) 
                return(return_status) 
            
                
            if ((is16BitPositive(a) and (not is16BitPositive(b)))):
                return(return_status) 
            
                
            if ((not is16BitPositive(a) and (not is16BitPositive(b)))):
                if (a < b): self.PTOS.write(0xFFFF)  
                return(return_status)
                 
        

        if (opcode == LONG_FETCH_OPC):
            self._address_history.append(c)

            self.PTOS.write(self.mem_read(scaledES + self.PTOS.read()))
            return(return_status)
        

        if (opcode == LONG_STORE_OPC):
            self._address_history.append(c)

            self.PSP.dec()
            literal = self.mem_read(scaledDS + self.PSP.read())
            self.mem_write(self.PTOS.read() + scaledES , literal)
            self.PSP.dec()
            self.PTOS.write( self.mem_read(self.PSP.read() + scaledDS) )
            return(return_status)
        
            
        if (opcode == LONG_TYPE_STORE_OPC):
            self._address_history.append(c)

            self.PSP.dec()
            type = self.mem_read(scaledDS + self.PSP.read())
            address = self.PTOS.read()
            self.mem_write_type(address + scaledES , type)
            self.PSP.dec()
            self.PTOS.write(self.mem_read(self.PSP.read() + scaledDS) )
            return(return_status)
        
            
        if (opcode == MUL_OPC):

            disassembly_string = "[%04X %04X] MUL | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)


            self.PSP.dec()
            self.PTOS.write(self.PTOS.read() * self.mem_read(scaledDS + self.PSP.read()))
            return(return_status)
        

        if (opcode == NEG_OPC):
            disassembly_string = "[%04X] NEG? | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)

            self._address_history.append(c)

            if (is16BitPositive(self.PTOS.read())):
                self.PTOS.write(0x0000)
            
            else:
                self.PTOS.write(0xFFFF)
            
            return(return_status)
        

        if (opcode == NOP_OPC):
            disassembly_string = "NOP" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            return(return_status)
        

        if (opcode == OR_OPC):

            disassembly_string = "[%04X %04X] OR | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PSP.dec()
            self.PTOS.write(self.PTOS.read() | self.mem_read(scaledDS + self.PSP.read()))
            return(return_status)
        

        if (opcode == OVER_OPC):
            disassembly_string = "[%04X %04X] OVER | %s"  % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(self.PSP.read() + scaledDS , self.PTOS.read())
            self.PTOS.write( self.mem_read((self.PSP.read() - 1 + scaledDS))  )
            self.PSP.inc()
            return(return_status)
        

        if (opcode == PLUS_OPC):

            disassembly_string = "[%04X %04X] + | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PSP.dec()
            self.PTOS.write(self.PTOS.read() + self.mem_read(scaledDS + self.PSP.read()))
            return(return_status)
        

        if (opcode == PLUS_PLUS_OPC):
            self._address_history.append(c)

            literal = self.mem_read(scaledDS + self.PTOS.read()) + 1
            self.mem_write(self.PTOS.read() + scaledDS , literal)
            self.PSP.dec()
            return(return_status)
        

        if (opcode == POPF_OPC):
            self._address_history.append(c)

            self.INT_CTL_LOW.write(self.PTOS.read())
            self.PSP.dec()

            self.PTOS.write(self.mem_read(scaledDS + self.PSP.read()))
            self.PSP.dec()
            return(return_status)
        

        if (opcode == PUSHF_OPC):
            self._address_history.append(c)

            # Write the self.PTOS To location where self.PSP points
            self.mem_write(scaledDS + self.PSP.read(), self.PTOS.read())
            self.PSP.inc()

            self.PTOS.write(self.INT_CTL_LOW.read())

            return(return_status)
        

        if (opcode == R_FETCH_OPC):
            disassembly_string = "[RTOS: %04X] R_FETCH | %s" % (rtos_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)

            self._address_history.append(c)

            self.mem_write(self.PSP.read() + scaledDS, self.PTOS.read() )
            self.PSP.inc()
            self.PTOS.write(self.RTOS.read())
            return(return_status)
        

        if (opcode == RET_OPC):
            disassembly_string = "RET [%04X] | %s"  % (rtos_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PC.write(self.RTOS.read())
            self.RSP.dec()
            self.RTOS.write( self.mem_read(self.RSP.read() + scaledDS) )
            return(return_status)
        

        if (opcode == RETI_OPC):
            self._address_history.append(c)

            self.RSP.dec()

            H = self.mem_read( self.RSP.read() + scaledDS) 

            self.RSP.dec()
            self.INT_CTL_LOW.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.dec()
            self.PC.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.dec()
            self.PTOS.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.dec()
            self.PSP.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.dec()
            self.ES.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.dec()
            self.CS.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.dec()
            self.DS.write(self.mem_read(self.RSP.read() + scaledDS))

            self.RSP.write(H)

            return(return_status)
        

        if (opcode == RP_FETCH_OPC):
            disassembly_string = "[RSP: %04X] RP_FETCH | %s" % (rsp_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(self.PSP.read() + scaledDS , self.PTOS.read())
            self.PTOS.write(self.RSP.read())
            self.PSP.inc()
            return(return_status)
        

        if (opcode == RP_STORE_OPC):
            right_operand = self.PTOS.read()
            disassembly_string = "[PTOS: %04X] RP_STORE | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.RSP.write(self.PTOS.read())
            self.PSP.dec()
            self.PTOS.write( self.mem_read( self.PSP.read() + scaledDS) )
            return(return_status)
        

        if (opcode == S_LESS_OPC):
            self._address_history.append(c)

            # usage a b S_LESS
            self.PSP.dec()
            self.PTOS.read()
            a = self.mem_read(self.PSP.read() + scaledDS) 
            b = self.PTOS.read()


            # OK with signed vals
            self.PTOS.write(0)
            if ((is16BitPositive(a) and (is16BitPositive(b)))):
                if (a < b): 
                    self.PTOS.write(0xFFFF) 
                
                return(return_status) 
            
                
            # This code was returning 0; seems wrong given this combination
            if ((not is16BitPositive(a) and (is16BitPositive(b)))):
                self.PTOS.write(0x0000) 
                self.PTOS.write(0xFFFF) 
                return(return_status) 
            
                
            if ((is16BitPositive(a) and (not is16BitPositive(b)))):
                return(return_status) 
            
                
            if ((not is16BitPositive(a) and (not is16BitPositive(b)))):
                if (a < b): self.PTOS.write(0xFFFF)  
                return(return_status)
            

            printf("FATAL Error in S_LESS a is %X b is %X\n", a, b)
            exit(1)
                
        
        if (opcode == SLL_OPC):
            self._address_history.append(c)

            self.PTOS.write((self.PTOS.read() << 1) & 0xFFFF)
            return(return_status)
        

        if (opcode == SP_FETCH_OPC):
            disassembly_string = "[PSP: %04X] SP_FETCH | %s" % (psp_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(self.PSP.read() + scaledDS , self.PTOS.read())
            self.PTOS.write(self.PSP.read())
            self.PSP.inc()
            return(return_status)
        

        if (opcode == SP_STORE_OPC):
            disassembly_string = "[PTOS: %04X] SP_STORE | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PSP.write(self.PTOS.read())
            return(return_status)
        

        if (opcode == SRA_OPC):
            self._address_history.append(c)

            signBit = self.PTOS.read() & 0x8000
            self.PTOS.write((self.PTOS.read() >> 1) | signBit)
            return(return_status)
        

        if (opcode == SRL_OPC):
            self._address_history.append(c)

            self.PTOS.write((self.PTOS.read() >> 1))
            return(return_status)
        

        if (opcode == STORE_OPC):
            disassembly_string = "[%04X %04X] STORE | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)




            self.PSP.dec()
            literal = self.mem_read(scaledDS + self.PSP.read())
            self.mem_write(self.PTOS.read() + scaledDS , literal)
            self.PSP.dec()
            self.PTOS.write( self.mem_read(self.PSP.read() + scaledDS) )
            return(return_status)
        
            
        if (opcode == STORE2_OPC):
            disassembly_string = "[%04X %04X] STORE2 | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)




            self.PSP.dec()

            val = self.PTOS.read()
            # This addr is only the 16 bit offset !!!
            # which is why we have to add the DS offset
            addr = self.mem_read(scaledDS + self.PSP.read())
            addr += scaledDS

            self.mem_write(addr , val)
            self.PSP.dec()

            self.PTOS.write( self.mem_read(self.PSP.read() + scaledDS) )
            return(return_status)
        
            
        if (opcode == SUB_OPC):

            disassembly_string = "[%04X %04X] - | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PSP.dec()
            self.PTOS.write(self.mem_read(scaledDS + self.PSP.read()) - self.PTOS.read())
            return(return_status)
        

        if (opcode == SWAP_OPC):
            disassembly_string = "[%04X %04X] SWAP | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)

            self._address_history.append(c)

            literal = self.PTOS.read()
            self.PTOS.write( self.mem_read(self.PSP.read() - 1 + scaledDS) )
            addr = (self.PSP.read() - 1) + scaledDS
            self.mem_write(addr, literal)
            return(return_status)
        

        if (opcode == SYSCALL_OPC):
            disassembly_string = "SYSCALL" 
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            H = self.RSP.read()

            self.mem_write(self.RSP.read() + scaledDS , self.DS.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.CS.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.ES.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.PSP.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.PTOS.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.PC.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , self.INT_CTL_LOW.read())

            self.RSP.inc()
            self.mem_write(self.RSP.read() + scaledDS , H)

            self.RSP.inc()
            self.INT_CTL_LOW.write(self.INT_CTL_LOW.read() & 0xFFFE)

            self.PC.write(0xFD02)
            self.CS.write(0x0000)
            return(return_status)
        

        if (opcode == TO_DS_OPC):
            self._address_history.append(c)

            self.DS.write(self.PTOS.read())
            self.PSP.dec()
            self.PTOS.write(self.mem_read(scaledDS + self.PSP.read()) - self.PTOS.read())
            return(return_status)
        

        if (opcode == TO_ES_OPC):
            self._address_history.append(c)

            self.ES.write(self.PTOS.read())
            self.PSP.dec()
            self.PTOS.write(self.mem_read(scaledDS + self.PSP.read()) - self.PTOS.read())
            return(return_status)
        

        if (opcode == TO_R_OPC):
            disassembly_string = "[PTOS: %04X] TO_R | %s" % (right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.mem_write(self.RSP.read() + scaledDS , self.RTOS.read())
            self.RSP.inc()
            self.RTOS.write(self.PTOS.read())
            self.PSP.dec()
            self.PTOS.write( self.mem_read(self.PSP.read() + scaledDS) )
            return(return_status)
        

        if (opcode == UM_PLUS_OPC):
            self._address_history.append(c)

            literal = self.PTOS.read() + self.mem_read(self.PSP.read() -1 + scaledDS) 
            self.PTOS.write((literal & 0x10000) >> 16)
            self.mem_write(self.PSP.read() - 1 + scaledDS, literal & 0xFFFF)
            return(return_status)
        

        if (opcode == XOR_OPC):
            disassembly_string = "[%04X %04X] XOR | %s" % (left_operand, right_operand, stack_string)
            c = CPUStatus(absolute_address, 
                self.CS.read(), self.DS.read(), self.PSP.read(), 
                self.RSP.read(), opcode, disassembly_string)
            self._address_history.append(c)

            self.PSP.dec()
            self.PTOS.write(self.mem_read(scaledDS + self.PSP.read()) ^ self.PTOS.read())
            return(return_status)
        

        print "FATAL Error - unknown opc %X at addr %X\n" % (opcode, self.PC.read() - 1)

    def set_interrupt_input(self, interrupt_input):
        self._interrupt_pin = interrupt_input
        
  
