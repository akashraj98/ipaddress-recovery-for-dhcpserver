import re
import os
import subprocess

#read dhcp lease file for ips
with open('/var/lib/dhcp/dhcpd.leases')as fh:
    fstring = fh.readlines()


#use regex to exract all the ips that are assigned by dhcp 
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
leaseip_lst =[]
for line in fstring:
    m = pattern.search(line)
    if m is not None and m.group() not in leaseip_lst:
        leaseip_lst.append(m.group())


#code pings ips from leaseip_list 
# checks if they reply to ping
# creates list of ips with no ping reply
noresp_ip=[]
with open(os.devnull, "wb") as limbo:
        for ip in leaseip_lst:
                result=subprocess.Popen(["ping", "-c", "1", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip, "inactive")
                        noresp_ip.append(ip)
                else:
                        print(ip, "active")

print(noresp_ip)


