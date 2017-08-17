#!/usr/bin/env python3

import picamera
import os
import RPi.GPIO as GPIO
from twython import Twython
from time import sleep, localtime, time

def feedTurtle():
    motor_pins = [6, 13, 19, 26]
    step1 = [6, 13]
    step2 = [13, 19]
    step3 = [19, 26]
    step4 = [26, 6]
    steps = [step1, step2, step3, step4]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pins, GPIO.OUT)

    for i in range(73):
        for step in steps:
            GPIO.output(step, True)
            sleep(.01)
            GPIO.output(step, False)

    GPIO.cleanup()

def feedTurtleBack():
    motor_pins = [6, 13, 19, 26]
    step1 = [6, 13]
    step2 = [13, 19]
    step3 = [19, 26]
    step4 = [26, 6]
    steps = [step4, step3, step2, step1]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pins, GPIO.OUT)

    for i in range(73):
        for step in steps:
            GPIO.output(step, True)
            sleep(.01)
            GPIO.output(step, False)

    GPIO.cleanup()

def feedTurtleExtra():
    motor_pins = [6, 13, 19, 26]
    step1 = [6, 13]
    step2 = [13, 19]
    step3 = [19, 26]
    step4 = [26, 6]
    steps = [step1, step2, step3, step4]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pins, GPIO.OUT)

    for i in range(1):
        for step in steps:
            GPIO.output(step, True)
            sleep(.01)
            GPIO.output(step, False)

    GPIO.cleanup()


if __name__ == '__main__':

    APP_KEY = 'your app key'
    APP_SECRET = 'your secret app key'
    OAUTH_TOKEN = 'your oauth token'
    OAUTH_TOKEN_SECRET = 'your secret oauth token'
    
    meals = 1
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    auth = twitter.get_authentication_tokens()
    
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    while True:
        if (localtime().tm_hour % 1, localtime().tm_min % 1, localtime().tm_sec % 5) == (0, 0, 0):
            timestamp = str(localtime().tm_hour) + str(localtime().tm_min) + str(localtime().tm_sec)
            twStatus = 'Turtle feed day and time: ' + str(localtime().tm_mday) + '/' + str(localtime().tm_mon) + '/' + str(localtime().tm_year) + ' ' + str(localtime().tm_hour) + ':' + str(localtime().tm_min) + ':' + str(localtime().tm_sec) + '.'
            print(twStatus)
            print('Number of meals is ' + str(meals) + '.')
            vidName = 'ttlfeed_' + timestamp
            camera.start_recording(vidName + '.h264')
            camera.wait_recording(1)
            feedTurtle()
            sleep(1)
            feedTurtleBack()
            sleep(1)
            feedTurtle()
            meals += 1
            sleep(1)
            if meals % 7 == 0:
                feedTurtleExtra()
                sleep(.1)
            camera.wait_recording(3)
            camera.stop_recording()
            os.system('MP4Box -add ' + vidName + '.h264 ' + vidName + '.mp4')

            video = open(vidName + '.mp4', 'rb')
            response = twitter.upload_video(media=video, media_type='video/mp4')
            twitter.update_status(status=twStatus, media_ids=[response['media_id']])
