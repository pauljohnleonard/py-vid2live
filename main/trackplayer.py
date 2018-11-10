
import math
import sys


mbpath=sys.path[0] + "/../../MusicBox/src"

sys.path.append(mbpath)
from MB import music,midi,setup
from MB.players import *



#  MetroNome


min_note = 30
max_note = 100
n_note = max_note-min_note

class TrackPlayer:

    def __init__(self):
        self.notesOn={}
        mid = midi.MidiEngine()
        # seq = MBmusic.Sequencer()   
        dev = mid.open_midi_out(setup.MIDI_OUT_NAMES)
        self.inst = midi.Instrument(dev.out,2)

    def on(self, pos, delta, vel, key):

        pitch =int( min_note + ( math.floor(pos[0]/self.rect[0]*n_note) ) )
    
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



