from pythonosc import udp_client
import math

min_note = 30
max_note = 100
n_note = max_note-min_note

thresh = 5


class DiffPlayer:

    def __init__(self,client):
        self.client = client
        self.notesOn={}

    def process(self,i,val):
        vvv = val[0]+val[1]+val[2]
        #print(vvv)
        isOn = i in self.notesOn
        on = vvv > thresh   
 
        if isOn and not on:
            del self.notesOn[i]
            return 0

        elif not isOn and on:
 
            val2=math.floor(min(127,(80*max(val[0],val[1],val[2])/thresh)))
            print(i,val2)
            self.client.send_message("/hit", [i, val2])
            self.notesOn[i] = True
            return val2