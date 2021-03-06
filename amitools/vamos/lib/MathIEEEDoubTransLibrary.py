from amitools.vamos.AmigaLibrary import *
from amitools.vamos.lib.lexec.ExecStruct import LibraryDef
from amitools.vamos.Log import *
import struct
import math

def fromDouble(number):
  hi=0
  lo=0
  st=struct.pack('>d',number)
  for c in st[0:4]:
    hi=(hi << 8) | ord(c)
  for c in st[4:8]:
    lo=(lo << 8) | ord(c)
  return (hi,lo)

#selco
def fromSingle(number):
  FloatVal=0
  st=struct.pack('>f',number)
  for c in st[0:4]:
#    print "ord(c)=" + str(ord(c))
    FloatVal=(FloatVal << 8) | ord(c)
#  print "FloatVal=" + str(FloatVal)  
  return FloatVal

def toDouble(hi,lo):
  st=""
  for i in range(0,4):
    st=st+chr(hi >> 24)
    hi=(hi << 8) & 0xffffffff
  for i in range(0,4):
    st=st+chr(lo >> 24)
    lo=(lo << 8) & 0xffffffff
  return struct.unpack('>d',st)[0]

#selco
def toSingle(hi):
  st=""
  for i in range(0,4):
    st=st+chr(hi >> 24)
    hi=(hi << 8) & 0xffffffff
  return struct.unpack('>f',st)[0]

class MathIEEEDoubTransLibrary(AmigaLibrary):
  name = "mathieeedoubtrans.library"

  def __init__(self, config):
    AmigaLibrary.__init__(self, self.name, LibraryDef, config)

  def setup_lib(self, ctx):
    AmigaLibrary.setup_lib(self, ctx)


#selco    
  def IEEEDPAcos(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.acos(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPAsin(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.asin(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPAtan(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.atan(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPCos(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.cos(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPCosh(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    try:
      Result=math.cosh(arg)
      (hi,lo)=fromDouble(Result)
    except OverflowError:
      (hi,lo)=(0x7fefffff, 0xffffffff)
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPExp(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    try:
      Result=math.exp(arg)
      (hi,lo)=fromDouble(Result)
    except OverflowError:
        (hi,lo)=(0x7fefffff, 0xffffffff)
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco
  # convert IEEE single to IEEE double
  def IEEEDPFieee(self,ctx):
    arg=toSingle(ctx.cpu.r_reg(REG_D0))
    DoubleVal=struct.unpack('d', struct.pack('d', arg))[0]
    (hi,lo)=fromDouble(DoubleVal)
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPLog(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    if arg < 0: # we should not crash for negative numbers!
      #(hi,lo)=fromDouble(float('nan'))
      (hi,lo)=(0xfff80000,0x00000000)
    else:

      try:
        Result=math.log(arg)
        (hi,lo)=fromDouble(Result)
      except ValueError:
        (hi,lo)=fromDouble(float('-inf'))

    ctx.cpu.w_reg(REG_D1,lo)
    return hi


#selco    
  def IEEEDPLog10(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    if arg < 0: # we should not crash for negative numbers!
      #(hi,lo)=fromDouble(float('nan'))
      (hi,lo)=(0xfff80000,0x00000000)
    else:

      try:
        Result=math.log10(arg)
        (hi,lo)=fromDouble(Result)
      except ValueError:
        (hi,lo)=fromDouble(float('-inf'))

    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPPow(self,ctx):
    y=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    x=toDouble(ctx.cpu.r_reg(REG_D2),ctx.cpu.r_reg(REG_D3))
    try:
      Result=math.pow(y,x);
      (hi,lo)=fromDouble(Result)
    except OverflowError:
      (hi,lo)=(0x7fefffff,0xffffffff)
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPSin(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.sin(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPSincos(self,ctx):
    ptr=ctx.cpu.r_reg(REG_A0)
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (Sin_hi,Sin_lo)=fromDouble(math.sin(arg))
    (Cos_hi,Cos_lo)=fromDouble(math.cos(arg))

    ctx.mem.access.w32(ptr,Cos_hi)   #write cos to ptr
    ctx.mem.access.w32(ptr+4,Cos_lo)

    ctx.cpu.w_reg(REG_D1,Sin_lo)
    return Sin_hi

#selco    
  def IEEEDPSinh(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    try:
      Result=math.sinh(arg)
      (hi,lo)=fromDouble(Result)
    except OverflowError:
        if arg<0:
          (hi,lo)=(0xffefffff, 0xffffffff)
        else:
          (hi,lo)=(0x7fefffff, 0xffffffff)  
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPSqrt(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    if arg < 0: # we should not crash for negative numbers!
#      (hi,lo)=fromDouble(float('nan')  # not a number (7ff80000 00000000)
      (hi,lo)=(0xfff80000,0)            # not a number, this is what is returned under AmigaOS3.9
    else:
      (hi,lo)=fromDouble(math.sqrt(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPTan(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.tan(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco    
  def IEEEDPTanh(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    (hi,lo)=fromDouble(math.tanh(arg))
    ctx.cpu.w_reg(REG_D1,lo)
    return hi

#selco
# double to single
  def IEEEDPTieee(self,ctx):
    arg=toDouble(ctx.cpu.r_reg(REG_D0),ctx.cpu.r_reg(REG_D1))
    FloatVal=struct.unpack('f', struct.pack('f', arg))[0]
    if FloatVal==float('inf'):
        ret=0x7f7fffff;
    elif FloatVal==float('-inf'):
        ret=0xff7fffff;
    else:
        ret=fromSingle(FloatVal)
    return ret


