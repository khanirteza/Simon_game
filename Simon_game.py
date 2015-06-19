#!/usr/bin/env python3

import RPi.GPIO as GPIO
import pygame
import time
import random

LED_1 = 22
LED_2 = 36
LED_3 = 38
LED_4 = 40

BTN_1 = 11
BTN_2 = 15
BTN_3 = 29
BTN_4 = 37

# setting up the GPIO as board layout
GPIO.setmode(GPIO.BOARD)

# setting up the output pin
GPIO.setup(LED_1, GPIO.OUT)
GPIO.setup(LED_2, GPIO.OUT)
GPIO.setup(LED_3, GPIO.OUT)
GPIO.setup(LED_4, GPIO.OUT)

# setting up the input pin
GPIO.setup(BTN_1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BTN_2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BTN_3, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BTN_4, GPIO.IN, GPIO.PUD_UP)

# setting up the sound
pygame.init()
one = pygame.mixer.Sound('snd_one.wav')
two = pygame.mixer.Sound('snd_two.wav')
three = pygame.mixer.Sound('snd_three.wav')
four = pygame.mixer.Sound('snd_four.wav')


try:
    # turn on all the LEDs
    def allOn():
        GPIO.output(LED_1, True)
        GPIO.output(LED_2, True)
        GPIO.output(LED_3, True)
        GPIO.output(LED_4, True)


    # turn off all the LEDs
    def allOff():
        GPIO.output(LED_1, False)
        GPIO.output(LED_2, False)
        GPIO.output(LED_3, False)
        GPIO.output(LED_4, False)


    # light sequence that is played after wrong move
    def lost():
        allOn()
        time.sleep(0.5)
        allOff()
        time.sleep(0.5)
        allOn()
        time.sleep(0.5)
        allOff()
        time.sleep(0.5)
        allOn()
        time.sleep(0.5)
        allOff()
        time.sleep(1)


    # starting a new game upon calling this function
    def game(randSeq):
        while True:
            allOn()
            time.sleep(.5)
            allOff()
            time.sleep(1)
            randSeq.append(random.randint(1,4))
            print(randSeq)			#just for debugging purpose
            for x in randSeq:
                if x == 1:
                    GPIO.output(LED_1, True)
                    one.play()
                elif x == 2:
                    GPIO.output(LED_2, True)
                    two.play()
                elif x == 3:
                    GPIO.output(LED_3, True)
                    three.play()
                elif x == 4:
                    GPIO.output(LED_4, True)
                    four.play()
                    
                time.sleep(1)
                allOff()
                time.sleep(0.25)

                
            cnt = 0
            
            while cnt < len(randSeq):
                btnPressed = False
                while btnPressed == False:
                    while GPIO.input(BTN_1) == False:
                        GPIO.output(LED_1, True)
                        inputVal = 1
                        btnPressed = True
                    while GPIO.input(BTN_2) == False:
                        GPIO.output(LED_2, True)
                        inputVal = 2
                        btnPressed = True
                    while GPIO.input(BTN_3) == False:
                        GPIO.output(LED_3, True)
                        inputVal = 3
                        btnPressed = True
                    while GPIO.input(BTN_4) == False:
                        GPIO.output(LED_4, True)
                        inputVal = 4
                        btnPressed = True
                        
                if inputVal == 1:
                    one.play()
                elif inputVal == 2:
                    two.play()
                elif inputVal == 3:
                    three.play()
                elif inputVal == 4:
                    four.play()
                    
                print(inputVal)		#just for debugging purpose
                allOff()
                if btnPressed == True and randSeq[cnt] != inputVal:
                    lost()
                    return 0

                cnt += 1


    # main game function, entry point of the program
    while True:
        randSeq = []
        random.seed(a=None, version=2)
        randSeq.append(random.randint(1,4))
        randSeq.append(random.randint(1,4))
        game(randSeq)
        
except KeyboardInterrupt:   # terminate the program and clean all the GPIO pin if ctrl+c is pressed
    print('Program terminated')
    
finally:
    pygame.quit()
    GPIO.cleanup()