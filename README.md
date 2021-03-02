# MLX90641 driver

![GitHub release (latest by date)](https://img.shields.io/github/v/release/melexis-fir/mlx90641-driver-py?label=github-latest-release-tag) ![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/melexis-fir/mlx90641-driver-py/build-test-publish?event=release&label=github-workflow) ![Lines of code](https://img.shields.io/tokei/lines/github/melexis-fir/mlx90641-driver-py)  

![PyPI](https://img.shields.io/pypi/v/mlx90641-driver) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mlx90641-driver) ![PyPI - License](https://img.shields.io/pypi/l/mlx90641-driver)  

![platform](https://img.shields.io/badge/platform-win10%20%7C%20linux%20PC%20%7C%20rasberry%20pi%204%20%7C%20Jetson%20Nano%20%7C%20beagle%20bone-lightgrey)  

# Intro

MLX90641 is a thermal camera (16x12 pixels) using Far InfraRed radiation from objects to measure the object temperature.  
https://www.melexis.com/mlx90641  
This python driver interfaces the MLX90641 and aims to facilitate rapid prototyping.

Currently this driver supports 3 type of interfaces:
- EVB90640-41 ==> https://www.melexis.com/en/product/EVB90640-41/
- Raspberry Pi with I2C on the 40-pin header.
- MCP2221 USB to I2C adaptor.

## Getting started

### Installation

```bash
pip install mlx90641-driver
```

https://pypi.org/project/mlx90641-driver/  
https://pypistats.org/packages/mlx90641-driver

Note This is a base package, therefore one of the below I2C drivers is still needed:  
- https://github.com/melexis-fir/mlx90641-driver-evb9064x-py
- https://github.com/melexis-fir/mlx90641-driver-devicetree-py  (/dev/i2c-<x>)
- https://github.com/melexis-fir/mlx90641-driver-mcp2221-py
- or make your own.

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
