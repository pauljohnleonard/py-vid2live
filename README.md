
#  If you want to USE OSC

To get python talking OSC

https://pypi.python.org/pypi/python-osc

Live control surface that understands OSC

https://github.com/stufisher/LiveOSC2


# MAX for live

Getting a MAX LIVE plugin to recieve OSC messages

http://music.arts.uci.edu/dobrian/Music215W11/examples.htm#Ex24

Third party plugin OSC-route can be found here

http://cnmat.berkeley.edu/downloads

I put the folder here and it seems to work

/Applications/Max.app/Contents/Resources/C74/externals



Open CV with python 



I looked at this
https://www.pyimagesearch.com/2016/12/19/install-opencv-3-on-macos-with-homebrew-the-easy-way/


but only did this

brew tap homebrew/science
brew install opencv3 --with-contrib --with-python3 


ipython
In [1]: import cv2

In [2]: cv2.__version__
Out[2]: '3.3.1'