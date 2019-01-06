#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import subprocess

pulse_start_time = 0

def play_vid():
    # os.system("omxplayer test.mp4 --no-osd")
    # os.system("omxplayer -o local --loop --no-osd test.mp4")
	cmd='omxplayer --loop --no-osd test.mp4'
	proc=subprocess.Popen(['omxplayer','--no-osd','--loop','test.mp4'])
	time.sleep(3)
	return proc

def stop_vid():
    os.system('killall omxplayer.bin')

try:
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 35
      PIN_ECHO = 38

      distance_threshold = 30
      
      video_playing = False
      
      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)
      
      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      time.sleep(0.05)

      video_playing = False
	
      while 1:
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
		
            time.sleep(1)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO)==0:
                  pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO)==1:
                  pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance = round(pulse_duration * 17150, 2)
            print "Distance:",distance,"cm"
            #print "video playing = ", video_playing
  
            # play video if not already playing
            if distance <= distance_threshold and video_playing==False:
                print "Playing video"
                video_playing = True
                play_vid()
            elif distance>=distance_threshold and video_playing==True:
		print "Stopping video"
		video_playing=False
		stop_vid()
finally:
      GPIO.cleanup()
      
