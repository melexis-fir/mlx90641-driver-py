import sys
from mlx90641 import *
import ctypes

def main():
    print ("start")
    dev = mlx90641()
    print ("dev", dev)

    # r = dev.i2c_init("/dev/i2c-1")
    # r = dev.i2c_init("ftdi://ftdi:2232/1")
    r = dev.i2c_init("mcp://mcp:2221/0")
    print ("init", r)
    r = dev.set_refresh_rate(1)
    print ("setRefreshRate", r)

    RR = dev.get_refresh_rate()
    print ("refresh rate: {}".format (RR))

    dev.dump_eeprom()
    dev.extract_parameters()
    
    for i in range(0,10):
        dev.get_frame_data()
        Ta = dev.get_TA()-8.0
        emissivity = 1

        To = dev.calculate_TO(emissivity, Ta)

        print("{:02d}: {}".format(i, ','.join(format(x, ".2f") for x in To)))


if __name__ == "__main__":
    main()
