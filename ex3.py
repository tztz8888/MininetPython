#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI

class SingleSwitchTopo(Topo):
    "Single Switch Connected to n nodes"
    def build(self, n=2):
        switch = self.addSwitch('s1')
        for h in range(n):
            host=self.addHost('h%s' %(h+1), cpu=0.5/n)
            self.addLink(host,switch, bw=10, delay='5ms', loss=5, max_queue_size=1000,use_htb=True)

def simpleTest():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net=Mininet(topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing connectivity"
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
