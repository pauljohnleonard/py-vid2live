import sys
import time

mbpath=sys.path[0] + "/../../MusicBox/src"

sys.path.append(mbpath)
from MB import MBmusic,MBmidi,MB
from MB.players import *

mid = MBmidi.MidiEngine()
seq = MBmusic.Sequencer()
dev = mid.open_midi_out(MB.MIDI_OUT_NAMES)

#  MetroNome
inst = MBmidi.Instrument(dev.out,9)



accent = MBmusic.NoteOn(61,100)
weak = MBmusic.NoteOn(60,80)
metro = MBmusic.Metro(0,4,seq,inst,accent,weak)


seq.start()
time.sleep(100)
    
