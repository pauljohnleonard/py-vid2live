# Files system mode:

Make sure the web cam is not in use then

# OSX

```
echo usbsd > /dev/cu.usbmodem1463 
```



# Host:
------


##  Devel  

jevois-deamon --serout=All


##  Platfrom


### Mount file system

jevois-usbsd  start
jevois-usbsd  stop




http://jevois.org/doc/ArduinoTutorial.html

JeVois allows you to store parameter settings and commands in a file named script.cfg stored in the directory of a module. The file script.cfg may contain any sequence of commands as you would type them interactively in the JeVois command-line interface.


# Send info log messages to None, send serial strings from module to Hard serial port:

setpar serlog None
setpar serout Hard


