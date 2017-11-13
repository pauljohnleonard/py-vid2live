from pythonosc import udp_client
import math

min_note = 30
max_note = 100
n_note = max_note-min_note

class Player:

    def __init__(self,client):
        self.client = client
        self.notesOn={}

    def on(self, pos, delta, vel, key):

        pitch = min_note + ( math.floor(pos[0]/self.rect[0]*n_note) )  
    
        print( pos )
        self.client.send_message("/note", [pitch , vel] )
        self.notesOn[key]=pitch

    def off(self, key):
        pitch=self.notesOn[key]
        #print(pitch,0)
        self.client.send_message("/note", [pitch, 0])


    def setWindow(self,rect):
        self.rect=rect
        print (rect)



