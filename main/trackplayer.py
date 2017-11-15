from pythonosc import udp_client
import math
import sys
import time

mbpath=sys.path[0] + "/../../MusicBox/src"

sys.path.append(mbpath)
from MB import MBmusic,MBmidi,MB
from MB.players import *



#  MetroNome


min_note = 30
max_note = 100
n_note = max_note-min_note

class TrackPlayer:

    def __init__(self):
        self.notesOn={}
        mid = MBmidi.MidiEngine()
        # seq = MBmusic.Sequencer()   
        dev = mid.open_midi_out(MB.MIDI_OUT_NAMES)
        self.inst = MBmidi.Instrument(dev.out,2)

    def on(self, pos, delta, vel, key):

        pitch = min_note + ( math.floor(pos[0]/self.rect[0]*n_note) )  
    
        print( pos )
        self.inst.note_on(pitch, vel)
        self.notesOn[key]=pitch

    def off(self, key):
        pitch=self.notesOn[key]
        #print(pitch,0)
        self.inst.note_off(pitch)


    def setWindow(self,rect):
        self.rect=rect
        print (rect)



