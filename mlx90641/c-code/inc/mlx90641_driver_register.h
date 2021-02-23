#ifndef __MLX90641_DRIVER_REGISTER_H__
#define __MLX90641_DRIVER_REGISTER_H__

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif


struct MLX90641DriverRegister_t
{
  char name_[64];
  void *(*MLX90641_get_i2c_handle_) (void);
  void (*MLX90641_set_i2c_handle_) (void *handle);

  void (*MLX90641_I2CInit_) (const char *port);
  void (*MLX90641_I2CClose_) (void);
  int  (*MLX90641_I2CRead_) (uint8_t slaveAddr, uint16_t startAddr, uint16_t nMemAddressRead, uint16_t *data);
  void (*MLX90641_I2CFreqSet_) (int freq);
  int  (*MLX90641_I2CGeneralReset_) (void);
  int  (*MLX90641_I2CWrite_) (uint8_t slaveAddr, uint16_t writeAddress, uint16_t data);
};

void mlx90641_register_driver(struct MLX90641DriverRegister_t *driver);
struct MLX90641DriverRegister_t *mlx90641_get_driver(const char *name);
struct MLX90641DriverRegister_t *mlx90641_get_active_driver(void);
int mlx90641_activate_driver(const char *name);

#ifdef __cplusplus
}
#endif

#endif // __MLX90641_DRIVER_REGISTER_H__
