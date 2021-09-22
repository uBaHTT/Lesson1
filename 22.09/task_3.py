import RPi.GPIO as GPiO

GPiO.setmode(GPiO.BCM)
GPiO.setup(22, GPiO.OUT)
p = GPiO.PWM(22, 1000)

try:
    while True:
        inputStr = input("Enter dutycycle between 0 and 100 ('q' to exit) > ")

        if inputStr.isdigit():
            value = int(inputStr)

            if value >= 101: 
                print("The value is too large, try again.")
                continue

            p.start(value)
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
    GPiO.output(22, GPiO.LOW)
    GPiO.cleanup(22)
    print("GPiO cleanup complited.")