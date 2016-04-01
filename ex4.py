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

        self.addLink(host[0],switch[0],bw=20, delay='50ms',loss=lossRate)

        self.addLink(switch[0],switch[1],bw=20, delay='50ms',loss=lossRate)
        self.addLink(switch[1],switch[2],bw=20, delay='50ms',loss=lossRate)
        self.addLink(switch[2],switch[3],bw=20, delay='50ms',loss=lossRate)

        self.addLink(host[1],switch[3],bw=20, delay='50ms',loss=lossRate)

def testTopo():
    "Create network and run simple performance tests"
    topo= CustomTopo(lossRate=1)
    net=Mininet(topo=topo,host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)

    print "Testing connectivity"
    #Connectivity test by sending 10 ping messages between each other
    for i in range(0,10):
       net.pingAll()

    print "test TCP bandwidth"
    for i in range(0,8):
        for j in range(0,8):
            if i<j:
                src, dst = net.hosts[i], net.hosts[j]
                src.cmd( 'telnet', dst.IP(), '5001' )
                print "testing", src.name, "<->", dst.name,
                bandwidth = net.iperf( [ src, dst ], seconds=10 )
                print bandwidth
                flush()

    print "test UDP loss rate at bandwidth 15 Mbps"
    for i in range(0,8):
        src=net.hosts[i]
        result=src.cmd('iperf -u -s &')
        pid = src.cmd('echo $!')
        for j in range(0,8):
            dst = net.hosts[j]
            if i!=j:
                print "client",dst.name,"-> server", src.name 
                ipsrc= src.IP()
                result1=dst.cmd('iperf -c %s -u -b 15M' %ipsrc)
                print result1
        print "Shutting down the iperf server\n"
        src.cmd('kill -9 $pid')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    testTopo()
