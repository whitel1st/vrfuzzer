#/usr/bin/python3


logo = (
"""
888     888 8888888b.  8888888888                                          
888     888 888   Y88b 888                                                 
888     888 888    888 888                                                 
Y88b   d88P 888   d88P 8888888 888  888 88888888 88888888  .d88b.  888d888 
 Y88b d88P  8888888P"  888     888  888    d88P     d88P  d8P  Y8b 888P"   
  Y88o88P   888 T88b   888     888  888   d88P     d88P   88888888 888     
   Y888P    888  T88b  888     Y88b 888  d88P     d88P    Y8b.     888     
    Y8P     888   T88b 888      "Y88888 88888888 88888888  "Y8888  888  
""")


# Fix for scapy error
# WARNING: No route found for IPv6 destination :: (no default route?). This affects only IPv6
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import scapy.all as scapy
import argparse
import netifaces
import os
from colorama import Fore

scapy.load_contrib('mpls')

parser = argparse.ArgumentParser(description='Argument')
parser.add_argument('iface', type=str, help='source interfaces which IP address will be used (IPv4 by default)')
parser.add_argument('dst', type=str, help='destination IP address (IPv4 by default)')
parser.add_argument('--ipv6', help='use IPv6 addresses', action='store_true')
args = parser.parse_args()

network_interfaces_list = netifaces.interfaces()


if args.iface not in network_interfaces_list:
	print('[Error] Wrong interface:',args.iface)
else:

	print(logo)

	# 17 
	# 2 	- is AF_INET (normal Internet addresses
	# 10	- is AF_INET6 (IPv6
	src_mac = netifaces.ifaddresses(args.iface)[17][0]['addr']
	if args.ipv6: src_ip = netifaces.ifaddresses(args.iface)[10][0]['addr']
	else: src_ip = netifaces.ifaddresses(args.iface)[2][0]['addr']

	dst_ip = args.dst
	# Get next hop ip address
	dst_next_hop = os.popen('ip route g 8.8.8.8 | grep via | cut -d " " -f 3 ').read()[:-1]
	dst_mac =  os.popen(' arp ' + dst_next_hop + ' |  awk \'{print $3}\' | tail -n 1').read()[:-1]

	print(Fore.BLUE + 'Source')
	print(' MAC\t',src_mac)
	print(' IP\t',src_ip)
	print('Destination')
	print(' MAC\t',dst_mac)
	print(' IP\t',dst_ip)
	print(' hop\t',dst_next_hop)

	ethernet = scapy.Ether(src=src_mac, dst=dst_mac)
	ip = scapy.IP(src=src_ip, dst=dst_ip)
	mpls = MPLS(label=10)
	icmp = scapy.ICMP()
	#udp = scapy.UDP(sport=646,dport=646)
	#scapy.sendp(ethernet/ip/mpls/ICMP, iface=args.iface)


	#network_interfaces = os.listdir('/sys/class/net/')