
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

def print_tempo_handler(unused_addr, args, tempo):
  print("[{0}] ~ {1}".format(args[0], tempo))


if __name__ == "__main__":

  ip="127.0.0.1"
 
  disp = dispatcher.Dispatcher()
 
  disp.map("/live/tempo", print_tempo_handler, "Tempo")

  server = osc_server.ThreadingOSCUDPServer(
      (ip, 9000), dispatcher)
  print("Serving on {}".format(server.server_address))
  # server.serve_forever()
  server_thread = threading.Thread(target=server.serve_forever)
  server_thread.start()
 
  client = udp_client.SimpleUDPClient(ip, 7000)

  cnt=0
  while(1):
    client.send_message("/noteoff", cnt+50)
    time.sleep(1)
    cnt= (cnt+1)%10
    client.send_message("/noteon", [cnt+50 , 80+cnt+5])
