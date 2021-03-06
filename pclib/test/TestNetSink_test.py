#=========================================================================
# TestNetSink_test.py
#=========================================================================

from __future__ import print_function

import pytest

from pymtl        import *
from pclib.test   import TestSource, TestNetSink
from pclib.ifcs import InValRdyBundle, OutValRdyBundle, NetMsg

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------
class TestHarness( Model ):

  def __init__( s, dtype, src_msgs, sink_msgs, src_delay, sink_delay ):

    # Instantiate models

    s.src  = TestSource  ( dtype, src_msgs,  src_delay  )
    s.sink = TestNetSink ( dtype, sink_msgs, sink_delay )

    # Connect

    s.connect( s.src.out,  s.sink.in_  )
    s.connect( s.src.done, s.sink.done )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace() + " | " + s.sink.line_trace()

#-------------------------------------------------------------------------
# Message Creator
#-------------------------------------------------------------------------
def mk_msg( src, dest, seqnum, payload ):
  msg         = NetMsg( 4, 16, 32 )
  msg.src     = src
  msg.dest    = dest
  msg.seqnum  = seqnum
  msg.payload = payload
  return msg

#-------------------------------------------------------------------------
# TestNetSink unit test - Inorder Messages
#-------------------------------------------------------------------------
def inorder_msgs():

  # Test messages

  test_msgs = [

      #       dest src seqnum payload
      mk_msg( 1,   0,  0,     0x00000100 ),
      mk_msg( 1,   0,  1,     0x00000101 ),
      mk_msg( 1,   0,  2,     0x00000102 ),
      mk_msg( 1,   0,  3,     0x00000103 ),
      mk_msg( 2,   1,  0,     0x00000210 ),
      mk_msg( 2,   1,  1,     0x00000211 ),
      mk_msg( 2,   1,  2,     0x00000212 ),
      mk_msg( 2,   1,  3,     0x00000213 ),
      mk_msg( 3,   2,  0,     0x00000320 ),
      mk_msg( 3,   2,  1,     0x00000321 ),
      mk_msg( 3,   2,  2,     0x00000322 ),
      mk_msg( 3,   2,  3,     0x00000323 ),
      mk_msg( 0,   3,  0,     0x00000030 ),
      mk_msg( 0,   3,  1,     0x00000031 ),
      mk_msg( 0,   3,  2,     0x00000032 ),
      mk_msg( 0,   3,  3,     0x00000033 ),
  ]

  return test_msgs[:], test_msgs[:]

#-------------------------------------------------------------------------
# TestSimpleNetSink unit test - Out of Order Messages
#-------------------------------------------------------------------------
def outoforder_msgs():

  # Test messages

  src_msgs = [

      #       dest src seqnum payload
      mk_msg( 1,   0,  3,     0x00000103 ),
      mk_msg( 1,   0,  1,     0x00000101 ),
      mk_msg( 2,   1,  1,     0x00000211 ),
      mk_msg( 1,   0,  2,     0x00000102 ),
      mk_msg( 2,   1,  0,     0x00000210 ),
      mk_msg( 3,   2,  3,     0x00000323 ),
      mk_msg( 2,   1,  2,     0x00000212 ),
      mk_msg( 3,   2,  1,     0x00000321 ),
      mk_msg( 0,   3,  2,     0x00000032 ),
      mk_msg( 3,   2,  2,     0x00000322 ),
      mk_msg( 0,   3,  0,     0x00000030 ),
      mk_msg( 3,   2,  0,     0x00000320 ),
      mk_msg( 0,   3,  1,     0x00000031 ),
      mk_msg( 2,   1,  3,     0x00000213 ),
      mk_msg( 0,   3,  3,     0x00000033 ),
      mk_msg( 1,   0,  0,     0x00000100 ),
  ]

  sink_msgs = [

      #       dest src seqnum payload
      mk_msg( 1,   0,  0,     0x00000100 ),
      mk_msg( 1,   0,  1,     0x00000101 ),
      mk_msg( 1,   0,  2,     0x00000102 ),
      mk_msg( 1,   0,  3,     0x00000103 ),
      mk_msg( 2,   1,  0,     0x00000210 ),
      mk_msg( 2,   1,  1,     0x00000211 ),
      mk_msg( 2,   1,  2,     0x00000212 ),
      mk_msg( 2,   1,  3,     0x00000213 ),
      mk_msg( 3,   2,  0,     0x00000320 ),
      mk_msg( 3,   2,  1,     0x00000321 ),
      mk_msg( 3,   2,  2,     0x00000322 ),
      mk_msg( 3,   2,  3,     0x00000323 ),
      mk_msg( 0,   3,  0,     0x00000030 ),
      mk_msg( 0,   3,  1,     0x00000031 ),
      mk_msg( 0,   3,  2,     0x00000032 ),
      mk_msg( 0,   3,  3,     0x00000033 ),
  ]

  return [ src_msgs, sink_msgs ]


#-------------------------------------------------------------------------
# TestSimpleNetSink test runner
#-------------------------------------------------------------------------
def run_test( dump_vcd, src_delay, sink_delay, src_msgs, sink_msgs ):

  # Instantiate and elaborate the model

  dtype = NetMsg( 4, 16, 32 )
  model = TestHarness( dtype, src_msgs, sink_msgs,
                       src_delay, sink_delay )
  model.vcd_file = dump_vcd
  model.elaborate()

  # Create a simulator using the simulation tool

  sim = SimulationTool( model )

  # Run the simulation

  print()

  sim.reset()
  while not model.done():
    sim.print_line_trace()
    sim.cycle()

  # Add a couple extra ticks so that the VCD dump is nicer

  sim.cycle()
  sim.cycle()
  sim.cycle()


ooo_msgs = outoforder_msgs()

#-------------------------------------------------------------------------
# test_inorder
#-------------------------------------------------------------------------
@pytest.mark.parametrize('src_delay,sink_delay',[
  ( 0, 0),
  ( 5, 0),
  ( 0, 5),
  (10, 5),
])
def test_inorder( dump_vcd, src_delay, sink_delay ):
  src_msgs, sink_msgs = inorder_msgs()
  run_test( dump_vcd, src_delay, sink_delay, src_msgs, sink_msgs )

#-------------------------------------------------------------------------
# test_outoforder
#-------------------------------------------------------------------------
@pytest.mark.parametrize('src_delay,sink_delay',[
  ( 0, 0),
  ( 5, 0),
  ( 0, 5),
  (10, 5),
])
def test_outoforder( dump_vcd, src_delay, sink_delay ):
  src_msgs, sink_msgs = outoforder_msgs()
  run_test( dump_vcd, src_delay, sink_delay, src_msgs, sink_msgs )


