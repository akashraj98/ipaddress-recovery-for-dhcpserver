import re
import subprocess
with open('/var/lib/dhcp/dhcpd.leases')as fh:
    fstring = fh.readlines()

pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
leaseip_lst =[]
for i in range(len(fstring)):
    m = pattern.search(fstring[i])
    if m is not None and m.group() not in leaseip_lst:
        leaseip_lst.append((m.group(),i))

