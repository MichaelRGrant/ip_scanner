#!/usr/bin/env python

import argparse
import re
import subprocess


def get_ip_from_mac(mac_addr):
    """
    Get an ip address of a connected device with known MAC address.
    """
    # ping all connected devices so arp will work for the listed mac address
    _ = subprocess.check_output(('nmap', '-sP', '192.168.1.0/24'))
    arp_res = subprocess.check_output(("arp", "-a")).decode('ascii')
    arp_list = arp_res.split('?')
    try:
        match_idx = [i for i, x in enumerate(arp_list) if re.search(mac_addr, str(x))][0]
    except IndexError:
        raise ValueError('IP Address not found for MAC address {}'.format(mac_addr))

    ip_address = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', arp_list[match_idx]).group(0)
    return ip_address


parser = argparse.ArgumentParser()
parser.add_argument('Mac', metavar='mac', type=str, help="mac address to search ip")
args = parser.parse_args()
mac_addr = args.Mac

print('IP Address at Mac\n{}'.format(get_ip_from_mac(mac_addr)))
