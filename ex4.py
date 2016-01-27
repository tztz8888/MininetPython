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

def perfTest():
    "Create network and run simple performance tests"
    topo=SingleSwitchTopo(n=4)
    net=Mininet(topo=topo,host=CPULimitedHost, link=TCLink)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing bw between h1 and h4"
    h1,h4=net.get('h1','h4')
    print "Now testing bandwidth"
    result=h1.cmd('iperf -u -s &')
    pid = h1.cmd('echo $!')
    print result

    print "Done running iperf on server, starting client now"
    result1=h4.cmd('iperf -c 10.0.0.1 -u -b 10000000')
    print result1

    print "Shutting down the iperf server"
    h1.cmd('kill -9 $pid')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()
