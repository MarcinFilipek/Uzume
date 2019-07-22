from PacketSender import PacketSender

class NucleoExpander:
    def __init__(self, name_serial, nop):
        '''
        Init drivera NucleoExpander
        :param nameSerial: name of serial port exp. 'COM10' or '/tty/ttyUSB'
        :param nop: number of packet in one send
        '''
        self.packetSerial = PacketSender(name_serial, nop)
        self.horizontal_servo_angle = 90
        self.vertical_servo_angle = 90

    def check_angle(self, angle):
        if angle < 0:
            return  0
        if angle > 180:
            return 180
        return angle

    def horizontal_servo_set_angle(self, angle):
        self.horizontal_servo_angle = self.check_angle(angle)
        self.packetSerial.add_packet(1, self.horizontal_servo_angle)

    def vertical_servo_set_angle(self, angle):
        self.vertical_servo_angle = self.check_angle(angle)
        self.packetSerial.add_packet(2, self.vertical_servo_angle)
