#include <stdio.h>
#include <string.h>

#include <stdlib.h>

#include "MLX90641_I2C_Driver_evb9064x.h"


static struct EVB9064x_t *g_handle;


struct MLX90641DriverRegister_t *
MLX90641_get_register_evb9064x(void)
{
  static struct MLX90641DriverRegister_t reg;

  strcpy(reg.name_, "mlx://evb:9064x/");
  reg.MLX90641_get_i2c_handle_  = MLX90641_get_i2c_handle_evb9064x;
  reg.MLX90641_set_i2c_handle_  = MLX90641_set_i2c_handle_evb9064x;
  reg.MLX90641_I2CInit_         = MLX90641_I2CInit_evb9064x;
  reg.MLX90641_I2CClose_        = MLX90641_I2CClose_evb9064x;
  reg.MLX90641_I2CRead_         = MLX90641_I2CRead_evb9064x;
  reg.MLX90641_I2CFreqSet_      = MLX90641_I2CFreqSet_evb9064x;
  reg.MLX90641_I2CGeneralReset_ = MLX90641_I2CGeneralReset_evb9064x;
  reg.MLX90641_I2CWrite_        = MLX90641_I2CWrite_evb9064x;
  return &reg;
}


void *
MLX90641_get_i2c_handle_evb9064x(void)
{
  return (void *)g_handle;
}


void
MLX90641_set_i2c_handle_evb9064x(void *handle)
{
  g_handle = (struct EVB9064x_t *)handle;
}


void MLX90641_I2CInit_evb9064x(const char *port) 
{
  const char *start = "mlx://evb:9064x/";
  if (strncmp(port, start, strlen(start)) != 0)
  {
    printf("ERROR: '%s' is not a valid port\n", port);
    return;
  }

  printf ("comport = '%s'\n", &port[strlen(start)]);
  g_handle = NULL;//todo!
}


void MLX90641_I2CClose_evb9064x(void)
{
  g_handle = NULL;
}


int MLX90641_I2CRead_evb9064x(uint8_t slaveAddr, uint16_t startAddr, uint16_t nMemAddressRead, uint16_t *data)
{
  // todo
  if (slaveAddr == startAddr) {}
  if (nMemAddressRead) {}
  if (data){}
  return -1;
}


void MLX90641_I2CFreqSet_evb9064x(int freq)
{
  if (freq){}
    // todo
}


int MLX90641_I2CGeneralReset_evb9064x(void)
{
  return -1; // todo
}


int MLX90641_I2CWrite_evb9064x(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data)
{
  int delay_ms = 0;
  if ((writeAddress & 0xFF00) == 0x2400) delay_ms = 10; // 10ms for EEPROM write!
  if (data == slaveAddr){}
  if (delay_ms) {}
  return -1; // todo
}
