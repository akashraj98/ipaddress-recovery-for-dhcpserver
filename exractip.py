import re

with open('/var/lib/dhcp/dhcpd.leases')as fh:
    fstring = fh.readlines()

print(fstring)
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
leaseip_lst =[]
for line in fstring:
    m = pattern.search(line)
    if m is not None and m.group() not in leaseip_lst:
        leaseip_lst.append(m.group())

print(leaseip_lst)