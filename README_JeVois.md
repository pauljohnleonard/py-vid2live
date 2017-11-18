# Files system mode to pu stuff on the JeVois

You need to make sure camera is not streaming 

## OSX

```
echo usbsd > /dev/cu.usbmodem1463 
```


## VirtualHost:

jevois-usbsd  start
jevois-usbsd  stop




# Running programms Host development 

jevois-deamon 


## To start turn off the video output stream

streamoff
setmapping2 YUYV 320 240 30.0 PJL MusicBox
streamon



# Running programms Host development



http://jevois.org/doc/ArduinoTutorial.html

JeVois allows you to store parameter settings and commands in a file named script.cfg stored in the directory of a module. The file script.cfg may contain any sequence of commands as you would type them interactively in the JeVois command-line interface.


# Send info log messages to None, send serial strings from module to Hard serial port:

setpar serlog None
setpar serout Hard


# Arduino mode

setmapping2 YUYV 320 240 30.0 PJL MusicBox
streamon 