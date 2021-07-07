import subprocess

#stop dhcp server
#check lease file and check for entry
#remove the entry carefully and start dhcp server
subprocess.call(["Systemctl stop isc-dhcp-server"])

with open('/var/lib/dhcp/dhcpd.leases')as fh:
    