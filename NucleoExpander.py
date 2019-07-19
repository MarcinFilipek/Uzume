from PacketSender import PacketSender

class NucleoExpander:
    def __init__(self, name_serial, nop):
        '''
        Init drivera NucleoExpander
        :param nameSerial: name of serial port exp. 'COM10' or '/tty/ttyUSB'
        :param nop: number of packet in one send
        '''
        self.packetSerial = PacketSender(name_serial, nop)

    def horizontal_servo_set_angle(self, angle):
        self.packetSerial.add_packet(1, angle)

    def vertical_servo_set_angle(self, angle):
        self.packetSerial.add_packet(2, angle)
