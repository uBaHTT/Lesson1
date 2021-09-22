import RPi.GPIO as GPiO

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
        inputStr = input("Enter a value between 0 and 255 ('q' to exit) > ")

        if inputStr.isdigit():
            value = int(inputStr)

            if value >= levels: 
                print("The value is too large, try again.")
                continue

            signal = bin2dac(value)
            voltage = value / levels * maxVoltage

            print("Entered value = {:^3} -> {}, output voltage = {:.2f}.".format(value, signal, voltage))
        elif inputStr == 'q':
            break
        else:
            print("Enter a positive integer.")
            continue
except KeyboardInterrupt:
    print("The program was stoped by the keyboard.")
else:
    print("No excrptions.")
finally:
    GPiO.output(dac, GPiO.LOW)
    GPiO.cleanup(dac)
    print("GPiO cleanup complited.")