"""
import time

with open('hello.txt', 'w') as f:
    f.write('Hello to this file')

time.sleep(60)
print(f.closed)


f = open('hellotwo.txt', 'w')
f.write('hello to this file')
time.sleep(60)
print(f.closed)
"""
#***********************
#***********************
#***********************

class Connect:
    def __init__(self, hostname):
        self.hostname = hostname

    def __enter__(self):
        print(f"Trying to connect to a server : {self.hostname}")

    def __exit__(self, exc_type, exc, tb):
        print(f'Updates finished! Restarting {self.hostname} ...')

    





