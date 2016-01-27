#!/usr/bin/python

from mininet.topo import LinearTopo
from mininet.net import Mininet
from mininet.cli import CLI


if __name__ == '__main__':
    Linear=LinearTopo(k=4)
    net=Mininet(topo=Linear)
    net.start()
    net.pingAll()
    CLI(net)
    net.stop()

