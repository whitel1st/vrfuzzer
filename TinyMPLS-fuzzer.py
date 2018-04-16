#/usr/bin/python3


logo = (
"""
   _    _    _    _    _    _    _    _  
  / \  / \  / \  / \  / \  / \  / \  / \ 
 ( V )( R )( F )( u )( z )( z )( e )( r )
  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/ 

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
parser.add_argument('labels', type=str, help='what labels to use. Example: 12-24,40,60')
parser.add_argument('--ipv6', help='use IPv6 addresses', action='store_true')
args = parser.parse_args()

network_interfaces_list = netifaces.interfaces()
labels_list = []

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

	print('Source')
	print(' MAC\t',src_mac)
	print(' IP\t',src_ip)
	print('Destination')
	print(' MAC\t',dst_mac)
	print(' IP\t',dst_ip)
	print(' hop\t',dst_next_hop)


	# Parse supplied lables range
	# and create array of all possible integers.
	# Not really elegant solution, but quick
	labels_h = args.labels.split(',')
	for label_supplied in labels_h:
		label = label_supplied.split('-')
		if len(label) == 1:
			labels_list.append(int(label_supplied))
		else:
			for l in range(int(label[0]),int(label[1])):
				labels_list.append(l)

	labels_list.sort()

	print('Lables')
	print(' count\t',len(labels_list))
	print(labels_list)


	# Initialize L2, L3 and ICMP
	ethernet = scapy.Ether(src=src_mac, dst=dst_mac)
	ip = scapy.IP(src=src_ip, dst=dst_ip)
	icmp = scapy.ICMP()

	# Send packets
	for label_in_list in labels_list:
		mpls = MPLS(label=label_in_list)
		#print('mpls',mpls,label_in_list)
		#scapy.sendp(ethernet/mpls/ip/icmp, iface=args.iface)
	#udp = scapy.UDP(sport=646,dport=646)


	#network_interfaces = os.listdir('/sys/class/net/')