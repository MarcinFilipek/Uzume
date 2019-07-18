import serial
import random
import time

ser = serial.Serial(
    port='COM10',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

if ser.isOpen():
    print(ser.name + ' is open...')


def senddata(command, data):
    print(command, data)
    command = command.to_bytes(2, byteorder='little')
    data = data.to_bytes(2, byteorder='little')
    ser.write([command[0], command[1], data[0], data[1]])


# for servo in range(2):
#     command = random.randint(1, 2048)
#     data = random.randint(1, 100)
#     print(command, data)
#     senddata(command, data)

sizePacket = 10
command = 1

liczbatransmisji = 5

input("Press Enter to continue...")
for l in range(liczbatransmisji):
    for i in range(sizePacket):
        if i == 0:
            data = random.randint(50, 150)
            senddata(command, data)
        else:
            senddata(0, 0)
    time.sleep(1)
    # input("Press Enter to continue...")
