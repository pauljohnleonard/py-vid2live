import libjevois as jevois
import cv2
import numpy as np
## Template
#
# This module can do something
#
# @author Paul John Leonard
# 
# @videomapping YUYV 640 480 22.0 YUYV 640 480 22.0 JeVois PythonDiceCounter
# @email pauljohnleonard\@gmail.com
# @address 
# @copyright Copyright (C) 2017 by Paul JohnLeonard
# @mainurl http://jevois.org
# @supporturl http://jevois.org/doc
# @otherurl http://iLab.usc.edu
# @license GPL v3
# @distribution Unrestricted
# @restrictions None
# @ingroup modules

class PythonTemplate:
    # ###################################################################################################
    ## Constructor
    def __init__(self):
        pass
        
    # ###################################################################################################
    ## Process function with no USB output
    def process(self, inframe):
        jevois.LFATAL("process no usb not implemented")
    
    # ###################################################################################################
    ## Process function with USB output
    def process(self, inframe, outframe):
        # Get the next camera image (may block until it is captured) and convert it to OpenCV BGR (for color output):
        pass