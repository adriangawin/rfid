import signal
import time
import requests
import json
import os
import MySQLdb
from display import *
import uuid

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal, frame):
    global run
    print ("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()

signal.signal(signal.SIGINT, end_read)

print ( "Program started..." )

lcd_init()

while run :
    ( error , data ) = rdr.request()
    if not error :
        print ( "-> Card detected" )
        print ( "-> Type of RFID card: " + str(data) )

        ( error, uid ) = rdr.anticoll()
        if error :
            print ( "-> error with anticolision")
        else :
            print ( "-> anticollision passed" )
            print str(uid)
            util.set_tag(uid)
            util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

            db = MySQLdb.connect("localhost", "adrian", "sandra34", "systemdb")
            cur = db.cursor()

            sql = """SELECT * from users"""

            try:
                cur.execute(sql)
                for row in cur.fetchall():
                    if (str(uid) == str(row[3]) ) :
                        id = str(row[0])
                        name = str(row[1]) + " " + str(row[2])
                        print name
                        lcd_string(str(row[0]) + " " + str(row[1]), LCD_LINE_1)
                        cur.execute('select * from events where id = "' + id + '"')
                        if cur.rowcount == 0 :
                            cur.execute('insert into events (id, event, picture) values (' + id + ', "come", "/picture/")')
                            db.commit()
                        else :
                            last = "test"
                            for last in cur.fetchall():
                                pass
                            if last[1] == "come" :
                                lcd_string("Bye", LCD_LINE_2)
                                path = "/pictures/" + str(uuid.uuid4())
                                os.system("fswebcam --no-banner -r 640x480 /home/pi/web" + path)
                                cur.execute('insert into events (id, event, picture) values (' + id + ', "leave", "' + path +'")')
                                db.commit()
                            else :
                                lcd_string("Welcome", LCD_LINE_2)
                                path = "/pictures/" + str(uuid.uuid4())
                                os.system("fswebcam --no-banner -r 640x480 /home/pi/web" + path)
                                cur.execute('insert into events (id, event, picture) values (' + id + ', "come", "' + path +'")')
                                db.commit()
                        lcd_string("", LCD_LINE_1)
                        lcd_string("", LCD_LINE_2)

                        
            except:
                print "Error"
            
            
            #print "User: " + j_array["name"]
            #if ( j_array["name"] != "" ) :
            #    os.system("fswebcam --no-banner -r 640x480 /home/pi/Desktop/photo-"+j_array["name"])
            #util.deauth()

        time.sleep(2)
    time.sleep(0.1)
