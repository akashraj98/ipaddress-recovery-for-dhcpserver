import re,time
import os
import subprocess

LEASE_PATH= '/var/lib/dhcp/dhcpd.leases'

# read dhcp lease file for ips
with open(LEASE_PATH)as fh:
    fstring = fh.readlines()

#use regex to exract all the ips that are assigned by dhcp 
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
leaseip_lst =[]
for index in range(len(fstring)):
    m = pattern.search(fstring[index])
    if m is not None and m.group() not in leaseip_lst:
        leaseip_lst.append((m.group(),index))


#PINGS IP from lease list and check
# checks if they reply to ping
# creates list of ips with no ping reply
noresp_ip=[]
resp_ip =[]
with open(os.devnull, "wb") as limbo:
        for ip in leaseip_lst:
                result=subprocess.Popen(["ping", "-c", "1", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip, "inactive")
                        noresp_ip.append(ip)
                else:
                        print(ip, "active")
                        resp_ip.append(ip)


###RECOVER_IP
#stop dhcp server
#chcek the lease lease file and check the entry
# remove noresp_ip carefully
#restart dhcp

for ip,line_no in leaseip_lst:
        if ip in noresp_ip:
                for j in range(line_no,line_no+8):
                        fstring[j] = '\n'

subprocess.call(["Systemctl stop isc-dhcp-server"])
subprocess.call(["mv",LEASE_PATH,LEASE_PATH+".bak"])
with open(LEASE_PATH, 'w') as f:
    for line in fstring:
        f.write(line)

subprocess.call(["Systemctl restart isc-dhcp-server"])

print("RECOVERING IPs ..................")
time.sleep(2)


#Creating Summary table
for ip in resp_ip:
        print(ip,"ASSIGNED")

for ip in noresp_ip:
        print(ip,"RECOVERED")