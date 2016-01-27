#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

class CustomTopo(Topo):
    "6 siwthes, 8 hosts"
    def build(self):
        switch=[]
        host=[]
        for s in range(0,6):
            switch.append( self.addSwitch('s%s' %(s+1)) )
        for h in range(0,8):
            host.append( self.addHost('h%s' %(h+1) ) )

        self.addLink(host[0],switch[0])
        self.addLink(host[1],switch[1])
        self.addLink(host[2],switch[2])
        self.addLink(host[3],switch[3])
        self.addLink(host[4],switch[3])
        self.addLink(host[5],switch[4])
        self.addLink(host[6],switch[5])
        self.addLink(host[7],switch[5])

        self.addLink(switch[0],switch[1],bw=10, delay='1ms',loss=3)
        self.addLink(switch[0],switch[2],bw=15, delay='2ms',loss=2)
        self.addLink(switch[1],switch[3],bw=20, delay='4ms',loss=1)
        self.addLink(switch[2],switch[4],bw=20, delay='4ms',loss=1)
        self.addLink(switch[4],switch[5],bw=40, delay='10ms',loss=2)

def testTopo():
    "Create network and run simple performance tests"
    topo= CustomTopo()
    net=Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testTopo()
