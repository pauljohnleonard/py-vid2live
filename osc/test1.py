
import argparse
import random
import time
import threading

from pythonosc import osc_message_builder
from pythonosc import udp_client

import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

if __name__ == "__main__":

  ip="127.0.0.1"
 
 
  client = udp_client.SimpleUDPClient(ip, 7000)

  cnt=0
  while(1):
    client.send_message("/note", [cnt+50 ,0 ])
    cnt = (cnt+1)%10
    client.send_message("/note", [cnt+50 , 100+cnt+5])
    client.send_message("/hit", [cnt+50 , 100+cnt+5])
    time.sleep(1)