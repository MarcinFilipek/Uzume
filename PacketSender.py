from Frame import Frame
from Frame import Packet
import serial

class PacketSender:
    def __init__(self, name_serial, nop):
        '''
        :param nameSerial: name of serial port exp. 'COM10' or '/tty/ttyUSB'
        :param nop: number of packet in frame
        '''
        self.frame = Frame(nop)
        self.serial = serial.Serial(
            port=name_serial,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        if self.serial.isOpen():
            print('[{}]: {} is open..'.format(__name__, name_serial))

    def log(self, text):
        print('[{}]: {}'.format(__name__, text))

    def add_packet(self, command, data):
        packet = Packet(command, data)
        if self.frame.is_full():
            self.send_frame()
            self.frame.clear()
        self.log('Add packet ({}, {})'.format(packet.command, packet.data))
        self.frame.add_packet(packet)

    def send_frame(self):
        max_size = self.frame.get_max_size()
        actual_size = self.frame.get_actual_size()

        if actual_size > 0:
            for i in range(actual_size):
                command = self.frame[i].command
                data = self.frame[i].data
                self.log('Send ({}, {})'.format(command, data))
                command = command.to_bytes(2, byteorder='little')
                data = data.to_bytes(2, byteorder='little')
                self.serial.write([command[0], command[1], data[0], data[1]])
            for l in range(max_size - actual_size):
                self.log('Send ({}, {})'.format(0, 0))
                self.serial.write([0, 0, 0, 0])
            self.frame.clear()
