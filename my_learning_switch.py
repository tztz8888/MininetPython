from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Tutorial (object):
  def __init__ (self, connection):
    # Keep track of the connection to the switch     
    self.connection = connection
    # This binds our PacketIn event listener
    connection.addListeners(self)
    self.mac_to_port = {}
  
  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet      
    "packet_in" is the ofp_packet_in object the switch had 
    sent to the controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    self.connection.send(msg)

  def act_like_lswitch (self, packet, packet_in, out_port):
    # We want to output to all ports -- we do that using the special
    # OFPP_ALL port as the output port.  (We could have also used
    # OFPP_FLOOD.)
    self.resend_packet(packet_in, out_port)

  def _handle_PacketIn (self, event):
    packet = event.parsed # This is the parsed packet data.
    src_mac = packet.src  # source mac address
    dst_mac = packet.dst  # destination mac address
    
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
    packet_in = event.ofp # The actual ofp_packet_in message.
    
    if dst_mac not in self.mac_to_port:
	out_port = of.OFPP_FLOOD
    else:
	out_port = self.mac_to_port[dst_mac]
	log.debug("received a packet for a known destination %s" % (str(dst_mac)))
    
    if src_mac not in self.mac_to_port:
	self.mac_to_port[src_mac]=event.port
	log.debug("received a packet from  unknown source %s" % (str(src_mac)))
    
    self.act_like_lswitch(packet, packet_in, out_port)


def launch ():
   def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
   core.openflow.addListenerByName("ConnectionUp", start_switch)
