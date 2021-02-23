#ifndef __MLX90641_I2C_DRIVER_DEVTREE_H__
#define __MLX90641_I2C_DRIVER_DEVTREE_H__

#include <stdint.h>

#include "mlx90641_driver_register.h"

#ifdef __cplusplus
extern "C" {
#endif

struct MLX90641DriverRegister_t *MLX90641_get_register_devtree(void);

void *MLX90641_get_i2c_handle_devtree(void);
void MLX90641_set_i2c_handle_devtree(void *handle);

void MLX90641_I2CInit_devtree(const char *port);
void MLX90641_I2CClose_devtree(void);
int MLX90641_I2CRead_devtree(uint8_t slaveAddr, uint16_t startAddr, uint16_t nMemAddressRead, uint16_t *data);
void MLX90641_I2CFreqSet_devtree(int freq);
int MLX90641_I2CGeneralReset_devtree(void);
int MLX90641_I2CWrite_devtree(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data);

#ifdef __cplusplus
}
#endif

#endif // __MLX90641_I2C_DRIVER_DEVTREE_H__
