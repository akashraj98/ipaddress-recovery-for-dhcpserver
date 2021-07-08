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
                result=subprocess.Popen(["ping", "-c", "1", "-W", "2", ip[0]],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip[0], "Malicious")
                        noresp_ip.append(ip[0])
                else:
                        print(ip[0], "Legitimate")
                        resp_ip.append(ip[0])


###RECOVER_IP
#stop dhcp server
#chcek the lease lease file and check the entry
# remove noresp_ip carefully
#restart dhcp
print(noresp_ip)
for ip,line_no in leaseip_lst:
        if ip in noresp_ip:
                for j in range(line_no,line_no+10):
                        fstring[j] = '\n'

start = time.time()

subprocess.run(["systemctl", "stop", "isc-dhcp-server"])
subprocess.run(["mv",LEASE_PATH,LEASE_PATH+".bak"])
with open(LEASE_PATH, 'w+') as f:
    for line in fstring:
        f.write(line)

subprocess.run(["systemctl", "restart", "isc-dhcp-server"])
end = time.time()
print("\nRECOVERING IPs ..................\n")
time.sleep(1)
for ip in noresp_ip:
        print(ip,end-start)
        
#Creating Summary table
print("\n__________IP Address Status_________\n")
for ip in resp_ip:
        print(ip,"ASSIGNED")

for ip in noresp_ip:
        print(ip,"RECOVERED")