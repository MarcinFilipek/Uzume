class Packet:
    def __init__(self, command=0, data=0):
        self.command = command
        self.data = data

    def set_command(self, com):
        self.command = com

    def set_data(self, data):
        self.data = data


class Frame:
    def __init__(self, size):
        self.packetsArray = []
        self.size = size

    def add_packet(self, packet):
        self.packetsArray.append(packet)

    def clear(self):
        self.packetsArray.clear()

    def is_full(self):
        return len(self.packetsArray) == self.size

    def get_max_size(self):
        return self.size

    def get_actual_size(self):
        return len(self.packetsArray)

    def __getitem__(self, index):
        return self.packetsArray[index]
