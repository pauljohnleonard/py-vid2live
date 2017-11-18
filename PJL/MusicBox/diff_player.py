import math
import libjevois as jevois


min_note = 30
max_note = 100
n_note = max_note-min_note

thresh = 40



class DiffPlayer:

    def __init__(self):      
        self.notesOn={}


    def process(self,i,val):
        vvv = val[0]+val[1]+val[2]
        #print(vvv)
        isOn = i in self.notesOn
        on = vvv > thresh   
 
        if isOn:
            if not on:
                del self.notesOn[i]
                jevois.sendSerial("n"+str(i)+"_0\n")
                return 0
            else:
                return self.notesOn[i]

        elif not isOn:
            if on:
 
                val2=math.floor(min(127,(80*max(val[0],val[1],val[2])/thresh)))
                #print(i,val2)

                self.notesOn[i] = val2
                jevois.sendSerial("n"+str(i)+"_"+str(val2)+"\n")
                return val2
            else:
                return 0
