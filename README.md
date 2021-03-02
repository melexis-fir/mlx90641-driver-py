# MLX90641 driver

![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/melexis-fir/mlx90641-driver-py/build-test-publish?event=release&label=release) ![Lines of code](https://img.shields.io/tokei/lines/github/melexis-fir/mlx90641-driver-py)  

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mlx90641-driver) ![PyPI](https://img.shields.io/pypi/v/mlx90641-driver)  

Milestones:
- [x] win 10 PC
- [x] Raspberry pi
- [x] Jetson Nano
- [x] linux pc

Note This is a base package, a low level I2C driver is still needed.  
- https://github.com/melexis-fir/mlx90641-driver-evb9064x-py
- https://github.com/melexis-fir/mlx90641-driver-devicetree-py  (/dev/i2c-<x>)
- https://github.com/melexis-fir/mlx90641-driver-mcp2221-py
- or make your own.

# Intro

This python driver for MLX90641 aims to facilitate the interfacing on a PC.

Currently this driver supports 3 type of interfaces:
- EVB90640-41 ==> https://www.melexis.com/en/product/EVB90640-41/
- Raspberry Pi with I2C on any GPIO pin.
- MCP2221 USB to I2C adaptor.

## Getting started

### Installation

```bash
pip install mlx90641-driver
```

https://pypi.org/project/mlx90641-driver/
https://pypistats.org/packages/mlx90641-driver

### Running the driver demo

* Connect the EVB to your PC.  
* Open a terminal and run following command:  

```bash
mlx90641-dump-frame auto
```

This program takes 1 optional argument.

```bash
mlx90641-dump-frame <communication-port>
```

