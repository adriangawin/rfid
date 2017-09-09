#!/usr/bin/python3

import sys

sys.path.insert(0, "/home/pi/pi-rc522/ChipReader")

from pirc522 import RFID

import signal

import time



rdr = RFID()

util = rdr.util()

util.debug = True



while True:

    (error, data) = rdr.request()

    if not error:

        print ("\nDetected")



        (error, uid) = rdr.anticoll()

        if not error:

            #Print UID

            print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

            rdr.write(0, 07);
	    (error, data) = rdr.read(0)
	    if not error:
		print ("Data" + str(data))

            time.sleep(1)


    

