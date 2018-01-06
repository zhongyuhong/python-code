# Using Hexiwear with Python
# Script to get the device data and append it to a file
# Usage
# python GetData.py <device>
# e.g. python GetData.py "00:29:40:08:00:01"
import pexpect
import time
import sys
import os
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# ---------------------------------------------------------------------
# function to transform hex string like "0a cd" into signed integer
# ---------------------------------------------------------------------
def hexStrToInt(hexstr):
    val = int(hexstr[0:2],16) + (int(hexstr[3:5],16)<<8)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val
# ---------------------------------------------------------------------

DEVICE = "F2:BE:D4:2F:E9:9A"   # device #24

if len(sys.argv) == 2:
  DEVICE = str(sys.argv[1])

# Run gatttool interactively.
child = pexpect.spawn("gatttool -I -t random -b "+DEVICE)

# Connect to the device.
print("Connecting to:"),
print(DEVICE)

NOF_REMAINING_RETRY = 3

while True:
  try:
    #child.sendline("connect {0}".format(DEVICE))
    child.sendline("connect")
    child.expect("Connection successful", timeout=5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  except pexpect.TIMEOUT:
    NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
    if (NOF_REMAINING_RETRY>0):
      print("timeout, retry...")
      continue
    else:
      print("timeout, giving up.")
      break
  else:
    print("Connected!")
    break

if NOF_REMAINING_RETRY>0 :
    while True:
        child.sendline("char-write-req 0x000c 0100")
        child.expect("Notification handle", timeout=None)
        child.expect("\r\n", timeout=None)
        #print(child.before[17:19])
        val=int(child.before[17:19],16)
        print(str(val))
        sock.sendto(str.encode(DEVICE+"-"+str(val)), (UDP_IP, UDP_PORT))

    sys.exit(0)
else:
    print("FAILED!")
    sys.exit(-1)
