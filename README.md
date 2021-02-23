# MLX90641 driver

This is a work-in-progess!

Currently only windows 10 is working with MCP2221 USB to I2C adaptor.

Milestones:
- [x] win 10 PC + mcp2221
- [x] Raspberry pi + devtree (/dev/i2c-1)
- [x] Jetson Nano + devtree
- [x] Raspberry pi + mcp2221
- [ ] linux pc + mcp2221
- [ ] windows 10 pc + EVB90640-41
- [ ] linux pc + EVB
- [ ] raspberry pi + EVB

# Intro

This python driver for MLX90641 aims to facilitate the interfacing on a PC.

Currently this driver supports 3 type of interfaces:
- EVB90640-41 ==> https://www.melexis.com/en/product/EVB90640-41/
- Raspberry Pi with I2C on any GPIO pin.
- MCP2221 USB to I2C adaptor.


## Dependencies

Driver:
- Python3
- pySerial


## Getting started

### Installation


```bash
pip install mlx90641
```

https://pypi.org/project/mlx90641/

### Running the driver demo

* Connect the EVB to your PC.  
* pen a terminal and run following command:  


```bash
mlx90641-dump-frame auto
```

This program takes 1 optional argument.

```bash
mlx90641-dump-frame <communication-port>
```

