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
    net=Mininet(topo=topo,host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing connectivity"
    #Connectivity test by sending 10 ping messages between each other
    #for i in range(0,10):
    #    net.pingAll()

    print "test TCP bandwidth"
    for i in range(0,8):
        for j in range(0,8):
            src, dst = net.hosts[i], net.hosts[j]
            print "Now testing bandwidth between h%s and h%s" %i%j
            result=src.cmd('iperf -u -s &')
            pid = src.cmd('echo $!')
            print result

            print "Done running iperf on server, starting client now"
            result1=dst.cmd('iperf -c 10.0.0.1 -u -b 10000000')
            print result1

    print "Shutting down the iperf server"
    h1.cmd('kill -9 $pid')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testTopo()
