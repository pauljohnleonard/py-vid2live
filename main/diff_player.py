from pythonosc import udp_client
import math
import sys

min_note = 30
max_note = 100
n_note = max_note-min_note

thresh = 40


mbpath=sys.path[0] + "/../../MusicBox/src"

sys.path.append(mbpath)
from MB import music,midi,setup
from MB.players import *



class DiffPlayer:

    def __init__(self):
      
        self.notesOn={}
        mid = midi.MidiEngine()
        # seq = MBmusic.Sequencer()   
        dev = mid.open_midi_out(setup.MIDI_OUT_NAMES)
        self.inst = midi.Instrument(dev.out,13)

    def process(self,i,val):
        vvv = val[0]+val[1]+val[2]
        #print(vvv)
        isOn = i in self.notesOn
        on = vvv > thresh   
 
        if isOn:
            if not on:
                del self.notesOn[i]
                return 0
            else:
                return self.notesOn[i]

        elif not isOn:
            if on:
 
                val2=math.floor(min(127,(80*max(val[0],val[1],val[2])/thresh)))
                print(i,val2)

                self.inst.note_on(i, val2)
                self.notesOn[i] = val2
                return val2
            else:
                return 0