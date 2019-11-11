def within_16_bits_check(v):
   if (not(v == (v & 0xFFFF))):
      e = BaseException("Bounds error for 16 bit value [%08X]" % (v))
      raise(e)

