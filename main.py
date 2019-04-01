# import RPi.GPIO as GPIO
# import time
import numpy as np
import curses
from playsound import playsound
import os
from os import path
import threading

import pygame
pygame.mixer.init()

SEQ_LENGTH = 5

# PWM OUTPUT
# ledN = 1
# ledW = 2
# ledS = 3
# ledE = 4


def empty():
    ''''''

t = threading.Timer(0, empty)
playingSong = ''

# Initialization
def setup():
    window = curses.initscr()
    curses.noecho()
    window.keypad(True)
    return window

def printToScreen(window, text, y=1):
    window.addstr(y, 0, text, curses.A_REVERSE)
    window.refresh()

# Loop
def loop(window):
    while True:
        sequence = getRandomSequence(SEQ_LENGTH)
        song = 1;
        printToScreen(window, str(sequence), 0)
        startAttempt(sequence, window)
        printToScreen(window, "new sequence is generated", 2)

def playFailureSound():
    global playingSong
    playingSong = 'fail'
    pygame.mixer.music.stop()
    pygame.mixer.music.load('./fail.wav')
    pygame.mixer.music.play()

def stopMusic():
    pygame.mixer.music.stop()

def stopMusicAfter(seconds):
    global t
    t.cancel() # cancel the old timer
    t = threading.Timer(seconds, stopMusic)
    t.start()

def continueMusic(song):
    global playingSong
    printToScreen(window, playingSong, 2)
    src = path.normpath(path.join(os.getcwd(), 'songs', song + '.wav'))

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(src)
        pygame.mixer.music.play()

    if pygame.mixer.music.get_busy() and not playingSong is song:
        printToScreen(window, 'playin', 3)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(src)
        pygame.mixer.music.play()

    playingSong = song
    stopMusicAfter(3.0)


def getDirection(k):
    if k == 259:
        return 'N'
    if k == 258:
        return 'S'
    if k == 260:
        return 'W'
    if k == 261:
        return 'E'

def startAttempt(sequence, window):
    for index, current_direction in enumerate(sequence, start=1):
        k = window.get_wch()
        current_input = getDirection(k)

        if current_input != current_direction:
            # reset attempt if direction is wrong
            printToScreen(window, 'wrong')
            playFailureSound()
            startAttempt(sequence, window)
            return
        else:
            printToScreen(window, 'right')
            continueMusic('BeatIt')

        curses.flushinp()
    printToScreen(window, 'sequence complete')

# Return a list of a certain length filled with directions
def getRandomSequence(length):

    directions = ['N', 'W', 'S', 'E']
    seq = np.random.choice(directions, length).tolist()

    return seq

# Execution
window = setup()
loop(window)
