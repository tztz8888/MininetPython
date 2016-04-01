#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import sys
flush = sys.stdout.flush

class CustomTopo(Topo):
    "6 siwthes, 8 hosts"
    def build(self,lossRate=1):
        switch=[]
        host=[]
        for s in range(0,4):
            switch.append( self.addSwitch('s%s' %(s+1)) )
        for h in range(0,2):
            host.append( self.addHost('h%s' %(h+1) ) )

        self.addLink(host[0],switch[0],bw=20, delay='5ms',loss=lossRate)

        self.addLink(switch[0],switch[1],bw=20, delay='5ms',loss=lossRate)
        self.addLink(switch[1],switch[2],bw=20, delay='5ms',loss=lossRate)
        self.addLink(switch[2],switch[3],bw=20, delay='5ms',loss=lossRate)

        self.addLink(host[1],switch[3],bw=20, delay='5ms',loss=lossRate)

def testTopo():
    "Create network and run simple performance tests"
    topo= CustomTopo(lossRate=1)
    net=Mininet(topo=topo,host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)


    print "test TCP bandwidth"
    for i in range(0,5) :
            src, dst = net.hosts[0], net.hosts[1]
            src.cmd( 'telnet', dst.IP(), '5001' )
            print "testing", src.name, "<->", dst.name,
            bandwidth = net.iperf( [ src, dst ], seconds=10 )
            print (bandwidth[0]+bandwidth[1])
            flush()

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testTopo()
