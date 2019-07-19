from NucleoExpander import NucleoExpander


def main():
    print("Uzume: Hello.")
    nucleo = NucleoExpander('COM10', 10)
    nucleo.horizontal_servo_set_angle(60)
    nucleo.vertical_servo_set_angle(57)
    nucleo.packetSerial.send_frame()
    print("Uzume: Bye.")


if __name__ == '__main__':
    main()
