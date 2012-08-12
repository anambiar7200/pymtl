import unittest
import sys
import os

from pymtl_test_examples import *
from pymtl_translate import *

import pymtl_debug
debug_verbose = False

class TestSlicesVerilog(unittest.TestCase):

  def setUp(self):
    self.temp_file = self.id().split('.')[-1] + '.v'
    self.fd = open(self.temp_file, 'w')
    self.compile_cmd = ("iverilog -g2005 -Wall -Wno-sensitivity-entire-vector"
                        "-Wno-sensitivity-entire-array " + self.temp_file)

  def translate(self, model):
    model.elaborate()
    if debug_verbose: pymtl_debug.port_walk(model)
    code = ToVerilog(model)
    code.generate( self.fd )
    self.fd.close()

  def test_rotator(self):
    self.translate( Rotator(8) )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_simplesplitter(self):
    self.translate( SimpleSplitter(8) )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_simplemerger(self):
    self.translate( SimpleMerger(8) )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_complexsplitter(self):
    self.translate( ComplexSplitter(16, 4) )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_complexmerger(self):
    self.translate( ComplexMerger(16, 4) )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  #def tearDown(self):
  #  os.remove(self.temp_file)


class TestCombinationalVerilog(unittest.TestCase):

  def setUp(self):
    self.temp_file = self.id().split('.')[-1] + '.v'
    self.fd = open(self.temp_file, 'w')
    self.compile_cmd = ("iverilog -g2005 -Wall -Wno-sensitivity-entire-vector"
                        "-Wno-sensitivity-entire-array " + self.temp_file)

  def translate(self, model):
    model.elaborate()
    if debug_verbose: pymtl_debug.port_walk(model)
    code = ToVerilog(model)
    code.generate( self.fd )
    self.fd.close()

  def test_onewire(self):
    model = OneWire(16)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_onewire_wrapped(self):
    model = OneWireWrapped(16)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_full_adder(self):
    model = FullAdder()
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_ripple_carry(self):
    model = RippleCarryAdder(4)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  #def tearDown(self):
  #  os.remove(self.temp_file)


class TestPosedgeClkVerilog(unittest.TestCase):

  def setUp(self):
    self.temp_file = self.id().split('.')[-1] + '.v'
    self.fd = open(self.temp_file, 'w')
    self.compile_cmd = ("iverilog -g2005 -Wall -Wno-sensitivity-entire-vector"
                        "-Wno-sensitivity-entire-array " + self.temp_file)

  def translate(self, model):
    model.elaborate()
    if debug_verbose: pymtl_debug.port_walk(model)
    code = ToVerilog(model)
    code.generate( self.fd )
    self.fd.close()

  def test_register(self):
    model = Register(16)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_register_wrapped(self):
    model = RegisterWrapper(16)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_register_chain(self):
    model = RegisterChain(16)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_register_splitter(self):
    model = RegisterSplitter(16)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  #def tearDown(self):
  #  os.remove(self.temp_file)

class TestCombAndPosedgeVerilog(unittest.TestCase):

  def setUp(self):
    self.temp_file = self.id().split('.')[-1] + '.v'
    self.fd = open(self.temp_file, 'w')
    self.compile_cmd = ("iverilog -g2005 -Wall -Wno-sensitivity-entire-vector"
                        "-Wno-sensitivity-entire-array " + self.temp_file)

  def translate(self, model):
    model.elaborate()
    if debug_verbose: pymtl_debug.port_walk(model)
    code = ToVerilog(model)
    code.generate( self.fd )
    self.fd.close()

  def test_incrementer(self):
    model = Incrementer()
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_counter(self):
    model = Counter(7)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_count_incr(self):
    model = CountIncr(7)
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_reg_incr(self):
    model = RegIncr()
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_incr_reg(self):
    model = IncrReg()
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_incr_reg(self):
    model = IncrReg()
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  def test_gcd(self):
    model = GCD()
    self.translate( model )
    x = os.system( self.compile_cmd )
    self.assertEqual( x, 0)

  #def tearDown(self):
  #  os.remove(self.temp_file)

if __name__ == '__main__':
  unittest.main()