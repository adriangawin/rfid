#!/usr/bin/python3

import sys
from pirc522 import RFID
import signal
import time
run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()

signal.signal(signal.SIGINT, end_read)

print("Strarting")
while run:
    (error, data) = rdr.request()
    if not error:
        print ("\nDetected, type: " + str(data))
        (error, uid) = rdr.anticoll()
        if  error:
	    print("Error with anticoll")
	else:
            print ("UID: "+str(uid[0])+"-"+str(uid[1])+"-"+str(uid[2])+"-"+str(uid[3]))
	    print ("my uid: "+str(uid))
	    print("\nSelecting tag")
	    error = util.set_tag(uid)
	    if error:
		print("Error with selecting tag")
	    else:
	    	error = util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
	   	if error :
		    print("Error with card auth")
		else :
		    util.read_out(1)
		    if error :
			print("Error with reading")
		    else :
	    		print("data(0): " + str(data))
			string = 'adrian'
			error = rdr.write(1, toHex(string))
			
			if error :
			    print("Error with writing")
			else :
		    	    print("writing completed")
		    	    util.read_out(1)
			    if error :
				print("Error with reading")
			    else :
		    		print("data: " + str(data))	    
	    util.deauth()
	    time.sleep(2)
	   
    

