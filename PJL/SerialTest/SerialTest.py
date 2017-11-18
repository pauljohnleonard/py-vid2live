import libjevois as jevois


class SerialTest:
    def __init__(self):
        self.cnt=0

    def process(self, inframe):
        frame = inframe.getCvBGR()

        if (self.cnt % 10) == 0:
            jevois.sendSerial(str(self.cnt))
        self.cnt += 1

    def process(self, inframe, outframe=None):
        frame = inframe.getCvBGR()

        if (self.cnt % 10) == 0:
            jevois.sendSerial(str(self.cnt))
        self.cnt += 1
                
        if not outframe is None:
            outframe.sendCvBGR(frame)


