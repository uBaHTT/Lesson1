import RPi.GPIO as GPiO
import time 
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
troykaModule = 17
comparator = 4
list_value = []
def dec2bin(dec):
    return [int(bit) for bit in bin(dec)[2:].zfill(bits)]

def bin2dac(value):
    signal = dec2bin(value)
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
    with open("settings.txt", "w") as settings_file:
        settings_file.write("")
    start_time = time.time()

    while True:
        a = 0
        b = 256
        value = int((a + b) / 2)
        while True:
            signal = bin2dac(value)
            voltage = value / levels * maxVoltage
            time.sleep(0.01)
            if b - a == 1:
                print("Идет процесс зарядки, ADC value = {:^3} -> {}, input voltage = {:.2f}".format(value, signal, voltage))
                break
            elif GPiO.input(comparator) == 1:
                a = value
                value = int((a + b) / 2)
            elif GPiO.input(comparator) == 0:
                b = value 
                value = int((a + b) / 2)
        list_value.append(value)
        value_str = [str(value)]
        with open("settings.txt", "a") as settings_file:
            settings_file.write("\n".join(value_str))
            settings_file.write("\n")

        if value >= 250:
            break

    GPiO.setup(troykaModule, GPiO.OUT, initial = GPiO.LOW)

    while True:
        a = 0
        b = 256
        value = int((a + b) / 2)
        while True:
            signal = bin2dac(value)
            voltage = value / levels * maxVoltage
            time.sleep(0.01)
            if b - a == 1:
                print("Идет процесс разрядки, ADC value = {:^3} -> {}, input voltage = {:.2f}".format(value, signal, voltage))
                break
            elif GPiO.input(comparator) == 1:
                a = value
                value = int((a + b) / 2)
            elif GPiO.input(comparator) == 0:
                b = value 
                value = int((a + b) / 2)
        list_value.append(value)
        value_str = [str(value)]
        with open("settings.txt", "a") as settings_file:
            settings_file.write("\n".join(value_str))
            settings_file.write("\n")

        if value <= 10:
            break
    
    stop_time = time.time()
    print("Длительность эксперимента:")
    print("{:.4f}".format(stop_time - start_time))
    print("Период измерений:")
    print("{:.1f}".format((stop_time - start_time) / 730))
    print("Часота дискретизации:")
    print("{}".format(1 / (stop_time - start_time)))
    print("Шаг по напряжению:")
    print("{}".format(3.3 / 256))
    
    plt.plot(list_value)
    plt.show()

except KeyboardInterrupt:
    print("The program was stoped by the keyboard.")
else:
    print("No excrptions.")
finally:
    GPiO.output(dac, GPiO.LOW)
    GPiO.cleanup(dac)
    print("GPiO cleanup complited.")