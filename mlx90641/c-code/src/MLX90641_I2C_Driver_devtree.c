#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "i2c.h"
#include "MLX90641_I2C_Driver_devtree.h"

static struct i2c_device g_handle_obj;
static struct i2c_device *g_handle;


struct MLX90641DriverRegister_t *
MLX90641_get_register_devtree(void)
{
  static struct MLX90641DriverRegister_t reg;

  strcpy(reg.name_, "/dev/i2c-");
  reg.MLX90641_get_i2c_handle_  = MLX90641_get_i2c_handle_devtree;
  reg.MLX90641_set_i2c_handle_  = MLX90641_set_i2c_handle_devtree;
  reg.MLX90641_I2CInit_         = MLX90641_I2CInit_devtree;
  reg.MLX90641_I2CClose_        = MLX90641_I2CClose_devtree;
  reg.MLX90641_I2CRead_         = MLX90641_I2CRead_devtree;
  reg.MLX90641_I2CFreqSet_      = MLX90641_I2CFreqSet_devtree;
  reg.MLX90641_I2CGeneralReset_ = MLX90641_I2CGeneralReset_devtree;
  reg.MLX90641_I2CWrite_        = MLX90641_I2CWrite_devtree;
  return &reg;
}


void *
MLX90641_get_i2c_handle_devtree(void)
{
  return (void *)g_handle;
}


void
MLX90641_set_i2c_handle_devtree(void *handle)
{
  g_handle = (struct i2c_device *)handle;
}


void MLX90641_I2CInit_devtree(const char *i2cPort) 
{
    if (g_handle == NULL)
    {
        g_handle = &g_handle_obj;
    }
    int bus;

    if (i2cPort == NULL)
    {
        i2cPort = "/dev/i2c-1";
    }
    if ((bus = i2c_open(i2cPort))==-1){
        return;
    }
    else{
        memset(g_handle, 0, sizeof(struct i2c_device));

        g_handle->bus = bus;       // Bus 1
        g_handle->addr = 0x33;     // Slave address is 0x33, 7bit
        g_handle->iaddr_bytes = 2;  // Device internal addres = 2 bytes
        g_handle->page_bytes = 16;  // Device are capable of 16 bytes per page 
    } 
}


void MLX90641_I2CClose_devtree(void)
{
    int bus;
    bus = g_handle->bus;
    i2c_close(bus);
}


int MLX90641_I2CRead_devtree(uint8_t slaveAddr, uint16_t startAddr, uint16_t nMemAddressRead, uint16_t *data)
{
    unsigned char buffer[1664];
    uint16_t *p;
    int i=0;

    memset(buffer, 0, sizeof(buffer));
    g_handle->addr = slaveAddr;
    
    p=data;

    i2c_ioctl_read(g_handle, startAddr, buffer, 2*nMemAddressRead);
    
    for (int cnt=0; cnt<nMemAddressRead; cnt++){
        i = cnt <<1;
        *p++=(uint16_t)buffer[i]*256 +(uint16_t)buffer[i+1];
    }
    return 0;
}


void MLX90641_I2CFreqSet_devtree(int freq)
{
  if (freq) {}
}


int MLX90641_I2CGeneralReset_devtree(void)
{
    return 0;
}


int MLX90641_I2CWrite_devtree(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data)
{
    unsigned char buffer[4];
    memset(buffer, 0, sizeof(buffer));
    
    buffer[0]=(char)((data>>8)&0x00FF);
    buffer[1]=(char)(data&0x00FF);

    g_handle->addr = slaveAddr;

    i2c_ioctl_write(g_handle, writeAddress, buffer, 4);

    return 0;
}
