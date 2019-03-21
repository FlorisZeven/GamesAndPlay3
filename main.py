# import RPi.GPIO as GPIO
# import time
import numpy as np

# PWM OUTPUT
# ledN = 1
# ledW = 2
# ledS = 3
# ledE = 4

# Initialization
def setup():
     return 0

# Loop
def loop():
    while True:
        sequence = getRandomSequence(5)
        song = 1;

        startAttempt(sequence)
        print("new sequence is generated")


def startAttempt(sequence):

    print(sequence)

    for current_direction in sequence:
        current_input = input("Press N,W,E,S")
        if current_input != current_direction:
            # reset attempt if direction is wrong
            print('wrong')
            startAttempt(sequence)
            return
        else:
            print('right')
    print('sequence complete')

def playSong():
    return 0

# Return a list of a certain length filled with directions
def getRandomSequence(length):

    directions = ['N', 'W', 'S', 'E']
    seq = np.random.choice(directions, length).tolist()

    return seq

# Execution
loop()