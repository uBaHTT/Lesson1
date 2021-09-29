import RPi.GPIO as GPiO
import time 

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4

def dec2bin(dec):
    return [int(bit) for bit in bin(dec)[2:].zfill(bits)]

def bin2dac(value):
    signal = dec2bin(value)
    print(len(signal))
    GPiO.output(dac, signal)
    return signal

def num2dac(value):
    signal = dec2bin(value)
    GPiO.output(dac, signal)
    return signal

GPiO.setmode(GPiO.BCM)
GPiO.setup(dac, GPiO.OUT, initial = GPiO.LOW)
GPiO.setup(troykaModule, GPiO.OUT, initial = GPiO.HIGH)
GPiO.setup(comparator, GPiO.IN)

try:
    while True:
        value = 128
        a = 128
        for i in range(8):
            signal = num2dac(value)
            comparatorValue = GPiO.input(comparator)
            if comparatorValue == 0:
                value += a
            else:
                value -= a
            a = int(a / 2)
        time.sleep(0.01)
        signal = num2dac(value)
        voltage = value / levels * maxVoltage
        print(value)

except KeyboardInterrupt:
    print("The program was stoped by the keyboard.")
else:
    print("No excrptions.")
finally:
    GPiO.output(dac, GPiO.LOW)
    GPiO.cleanup(dac)
    print("GPiO cleanup complited.")