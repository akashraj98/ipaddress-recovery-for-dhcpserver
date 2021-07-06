
import subprocess
import os

with open(os.devnull, "wb") as limbo:
        for n in range(100, 110):
                ip="192.168.0.{0}".format(n)
                result=subprocess.Popen(["ping", "-c", "1", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print(ip, "inactive")
                else:
                        print(ip, "active")

