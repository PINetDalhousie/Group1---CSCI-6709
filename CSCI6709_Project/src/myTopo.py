#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI

from mininet.topo import Topo


# from mininet.util import dumpNodeConnections


class create_topo(Topo):

    def __init__(self):
        Topo.__init__(self)

        switch_list = []

        for i in range(1, 7):
            host = self.addHost('h' + str(i))
            switch = self.addSwitch('s' + str(i))
            switch_list.append(switch)
            self.addLink(host, switch)

        
        for i in range(1, 6):
            self.addLink(switch_list[0], switch_list[i])
        


def runner():
    # Create and run a custom topo
    curr_topo = create_topo()
    net = Mininet(topo=curr_topo)

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    runner()

topos = {
    'create_topo' : create_topo
}



