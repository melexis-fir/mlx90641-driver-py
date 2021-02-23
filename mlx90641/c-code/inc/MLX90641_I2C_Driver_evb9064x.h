#ifndef __MLX90641_I2C_DRIVER_EVB9064X_H__
#define __MLX90641_I2C_DRIVER_EVB9064X_H__

#include <stdint.h>

#include "mlx90641_driver_register.h"

#ifdef __cplusplus
extern "C" {
#endif

struct MLX90641DriverRegister_t *MLX90641_get_register_evb9064x(void);

void *MLX90641_get_i2c_handle_evb9064x(void);
void MLX90641_set_i2c_handle_evb9064x(void *handle);

void MLX90641_I2CInit_evb9064x(const char *port);
void MLX90641_I2CClose_evb9064x(void);
int MLX90641_I2CRead_evb9064x(uint8_t slaveAddr, uint16_t startAddr, uint16_t nMemAddressRead, uint16_t *data);
void MLX90641_I2CFreqSet_evb9064x(int freq);
int MLX90641_I2CGeneralReset_evb9064x(void);
int MLX90641_I2CWrite_evb9064x(uint8_t slaveAddr, uint16_t writeAddress, uint16_t data);

#ifdef __cplusplus
}
#endif

#endif // __MLX90641_I2C_DRIVER_EVB9064X_H__
