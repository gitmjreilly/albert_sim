import re

def within_16_bits_check(v):
   if (not(v == (v & 0xFFFF))):
      e = BaseException("Bounds error for 16 bit value [%08X]" % (v))
      raise(e)

def valid_hex_word_check(s):
   if (not(re.match("^[0-9A-F]{4,4}$", s))):
      e = BaseException("[%s] is not a valid hex word" % (s))
      raise(e)

