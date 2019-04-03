# import RPi.GPIO as GPIO
# import time
import numpy as np
import curses
from playsound import playsound
import os
from os import path
import threading

from rpi_ws281x import Color
import leds

import pygame
pygame.mixer.init()

SEQ_LENGTH = 5
DIRECTIONS = ['N', 'W', 'S', 'E']
SONGS = ['BeatIt', 'AnotherOneBitesTheDust', 'HighwayToHell', 'NsInParis']

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
    leds.set(Color(0,0,0))
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
        song = getRandomSong()
        printToScreen(window, str(sequence), 0)
        startAttempt(sequence, window, song)
        printToScreen(window, "new sequence is generated", 2)

def playFailureSound():
    global playingSong
    playingSong = 'fail'
    pygame.mixer.music.stop()
    pygame.mixer.music.load('./fail.wav')
    pygame.mixer.music.play()

def stopMusic():
    pygame.mixer.music.pause()

def stopMusicAfter(seconds):
    global t
    t.cancel() # cancel the old timer
    t = threading.Timer(seconds, stopMusic)
    t.start()
    printToScreen(window, '   ', 4)

def continueMusic(song, seconds):
    global playingSong
    printToScreen(window, playingSong, 2)
    src = path.normpath(path.join(os.getcwd(), 'songs', song + '.wav'))

    if not pygame.mixer.music.get_busy():
        printToScreen(window, '!!!', 4)
        if not playingSong is song:
            pygame.mixer.music.load(src)
            pygame.mixer.music.play()
        else:
            printToScreen(window, 'resuming', 3)
            pygame.mixer.music.unpause()

    if pygame.mixer.music.get_busy():
        if not playingSong is song:
            printToScreen(window, 'playing', 3)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(src)
            pygame.mixer.music.play()
        else:
            printToScreen(window, 'resuming', 3)
            pygame.mixer.music.unpause()

    playingSong = song
    stopMusicAfter(seconds)

def getDirection(k):
    if k == 259:
        return 'N'
    if k == 258:
        return 'S'
    if k == 260:
        return 'W'
    if k == 261:
        return 'E'

def startAttempt(sequence, window, song):
    for index, current_direction in enumerate(sequence, start=1):
        k = window.get_wch()
        current_input = getDirection(k)

        if current_input != current_direction:
            # reset attempt if direction is wrong
            printToScreen(window, 'wrong')
            playFailureSound()
            leds.set(Color(255,0,0))
            startAttempt(sequence, window, song)
            return
        else:
            printToScreen(window, 'right')
            sec = 10.0 if index is len(sequence) else 2.0
            continueMusic(song, sec)
            leds.set(Color(0,255,0))

        curses.flushinp()
    leds.rb()
    leds.set(Color(0,0,0))
    printToScreen(window, 'sequence complete')

# Return a list of a certain length filled with directions
def getRandomSequence(length):

    return np.random.choice(DIRECTIONS, length).tolist()

def getRandomSong():
    return np.random.choice(SONGS, 1)[0]

# Execution
window = setup()
loop(window)
