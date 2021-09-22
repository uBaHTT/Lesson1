import RPi.GPIO as GPiO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3

def dec2bin(dec):
    return [int(bit) for bit in bin(dec)[2:].zfill(bits)]

def bin2dac(value):
    signal = dec2bin(value)
    GPiO.output(dac, signal)
    return signal


GPiO.setmode(GPiO.BCM)
GPiO.setup(dac, GPiO.OUT, initial = GPiO.LOW)

try:
    while True:
        inputStr = input("Enter 's' to start ('q' to exit) > ")

        if inputStr == 's':
            for value in range(511):
                signal = bin2dac(255 - abs(value - 255))
                time.sleep(0.05)
        elif inputStr == 'q':
            break
except KeyboardInterrupt:
    print("The program was stoped by the keyboard.")
else:
    print("No excrptions.")
finally:
    GPiO.output(dac, GPiO.LOW)
    GPiO.cleanup(dac)
    print("GPiO cleanup complited.")