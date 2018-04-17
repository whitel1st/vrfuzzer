```
  / \  / \  / \  / \  / \  / \  / \  / \ 
 ( V )( R )( F )( u )( z )( z )( e )( r )
  \_/  \_/  \_/  \_/  \_/  \_/  \_/  \_/ 
```

# Install

`pip3 install -r requirements.txt`


# Use

`vrfuzer.py <iface> <dst_ip_address> <mpls_labels>`
- `iface` - source interfaces which IP address will be used 
- `dst` - destination IP address 
- `labels` - what labels to use. Example: 12-24,40,60


Example 
`vrfuzzer.py  wlp3s0 10.0.0.1 4`


# Why

Initial setup
- Backbone MPLS area
	- R1 and R3 are Provider Edge routers
	- Both R1 and R3 had been set up wih MPLS L3VPN
- Two VRFs
	- Yellow with two routers: `YELLLOW0` and `YELLOW1`
	- Grenn with `GREEN0` and `GREEN1`



Test if there are any MPLS/VRF misconfig or vulnerability

