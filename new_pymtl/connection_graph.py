#=========================================================================
# connection_graph.py
#=========================================================================
# Classes used to construct the connection graph of a Model.

from helpers import get_nbits

from signals import InPort, Constant

#-------------------------------------------------------------------------
# ConnectionSlice
#-------------------------------------------------------------------------
class ConnectionSlice(object):
  def __init__( self, port, addr ):
    self.parent_port = port
    self._addr       = addr
    if isinstance( addr, slice ):
      assert not addr.step  # We dont support steps!
      self.nbits     = addr.stop - addr.start
    else:
      self.nbits     = 1

  def connect(self, target):
    connection_edge = ConnectionEdge( self, target )
    self.parent_port.connections   += [ connection_edge ]
    # TODO: figure out a way to get rid of this special case
    if not isinstance( target, int ):
      target.parent_port.connections += [ connection_edge ]
    return connection_edge

  @property
  def connections(self):
    return self.parent_port.connections
  @connections.setter
  def connections(self, value):
    self.parent_port.connections = value

  @property
  def width( self ):
    """Temporary"""
    return self.nbits

#-------------------------------------------------------------------------
# ConnectError
#-------------------------------------------------------------------------
# Exception raised for invalid connection parameters
class ConnectError(Exception):
  pass

#-------------------------------------------------------------------------
# ConnectionEdge
#-------------------------------------------------------------------------
# Class representing a structural connection between Signal objects.
class ConnectionEdge(object):

  def __init__( self, src, dest ):

    # Validate inputs, raise exceptions if necessary
    if   isinstance( src, int ):
      if get_nbits( src ) > dest.nbits:
        raise ConnectError("Constant is too big for target Signal!")
      else:
        src = Constant( dest.nbits, src )

    elif isinstance( dest, int ):
      if get_nbits( dest ) > src.nbits:
        raise ConnectError("Constant is too big for target Signal!")
      else:
        dest = Constant( src.nbits, dest )

    elif src.nbits != dest.nbits:
      raise ConnectError("Connecting signals with different bitwidths!")

    # Set the nbits attribute of the connection
    self.nbits = src.nbits

    # Source Node
    if isinstance( src, ConnectionSlice ):
      self.src_node = src.parent_port
    else:
      self.src_node = src
    self.src_slice  = src._addr

    # Destination Node
    if isinstance( dest, ConnectionSlice ):
      self.dest_node = dest.parent_port
    else:
      self.dest_node = dest
    self.dest_slice = dest._addr

    # Add ourselves to the src_node and dest_node connectivity lists
    # TODO: is this the right way to do this?
    src.connections  += [ self ]
    dest.connections += [ self ]

  #-----------------------------------------------------------------------
  # other
  #-----------------------------------------------------------------------
  # If given the src_node, return the dest_node.
  # If given the dest_node, return the src_node.
  # Assert if the provided node is neither the src_node or dest_node.
  def other( self, node ):
    assert self.src_node == node or self.dest_node == node
    if self.src_node == node:
      return self.dest_node
    else:
      return self.src_node

  #-----------------------------------------------------------------------
  # is_dest
  #-----------------------------------------------------------------------
  def is_dest( self, node ):
    return self.dest_node == node

  #-----------------------------------------------------------------------
  # is_src
  #-----------------------------------------------------------------------
  def is_src( self, node ):
    return self.src_node == node

  #-----------------------------------------------------------------------
  # is_internal
  #-----------------------------------------------------------------------
  # Return true if this connection belongs to the same parent module as
  # the provided node.
  def is_internal( self, node ):
    # Determine which node is the other in the connection
    other = self.other( node )

    # InPort connections to Constants are external, else internal
    if isinstance( self.src_node, Constant ):
      return not isinstance( self.dest_node, InPort )

    # Check if the connection is an internal connection for the node
    return (( self.src_node.parent == self.dest_node.parent ) or
            ( other.parent in node.parent._submodules ))

  #-----------------------------------------------------------------------
  # swap_direction
  #-----------------------------------------------------------------------
  # Swap the direction of the connection, the source becomes the
  # destination and vice versa.
  def swap_direction( self ):
    self.src_node,  self.dest_node  = self.dest_node,  self.src_node
    self.src_slice, self.dest_slice = self.dest_slice, self.src_slice

