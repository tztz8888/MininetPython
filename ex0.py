#!/usr/bin/python

from mininet.topo import LinearTopo
from mininet.net import Mininet


if __name__ == '__main__':
    Linear=LinearTopo(k=4)
    net=Mininet(topo=Linear)
    net.start()
    net.pingAll()
    net.stop()

