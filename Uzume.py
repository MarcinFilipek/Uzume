from NucleoExpander import NucleoExpander
import os


def main():
    print("Uzume: Hello.")
    nucleo = NucleoExpander(os.environ['SERIAL_PORT'], 10)
    nucleo.horizontal_servo_set_angle(40)
    nucleo.vertical_servo_set_angle(150)
    nucleo.packetSerial.send_frame()
    print("Uzume: Bye.")


if __name__ == '__main__':
    main()
