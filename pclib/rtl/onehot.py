#=======================================================================
# onehot.py
#=======================================================================

from pymtl import *

#-----------------------------------------------------------------------
# Mux
#-----------------------------------------------------------------------
class Mux( Model ):

  def __init__( s, nports, data_nbits ):

    s.sel = InPort ( data_nbits )
    s.in_ = [ InPort( data_nbits ) for x in range( nports ) ]
    s.out = OutPort( data_nbits )

    @s.combinational
    def logic():
      if not s.sel:
        s.out.value = 0
      else:
        for i in range( nports ):
          if s.sel[i]:
            s.out.value = s.in_[i]

  def line_trace( s ):
    str_ = ' | '.join( ['{} {}'.format( s.sel[i], in_ ) for i, in_
                        in enumerate( s.in_ ) ] )
    str_ += ' () {}'.format( s.out )
    return str_

#-----------------------------------------------------------------------
# Demux
#-----------------------------------------------------------------------
class Demux( Model ):

  def __init__( s, nports, data_nbits ):

    s.sel = InPort( data_nbits )
    s.in_ = InPort( data_nbits )
    s.out = [ OutPort( data_nbits ) for x in range( nports ) ]

    @s.combinational
    def logic():
      for i in range( nports ):
        s.out[i].value = s.in_ if s.sel[i] else 0

  def line_trace( s ):
    str_  = '{} {} () '.format( s.sel, s.in_ )
    str_ += ' | '.join( ['{}'.format( x ) for x in s.out ] )
    return str_
