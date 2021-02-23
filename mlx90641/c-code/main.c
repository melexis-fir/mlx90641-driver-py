#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include <stdint.h>

#include "MLX90641_I2C_Driver.h"
#include "MLX90641_API.h"
#include "mlx90641_driver_api_register.h"
#include "MLX90641_I2C_Driver_mcp2221.h"

#define MLX_I2C_ADDR 0x33

int main(void){

    mlx90641_register_driver(MLX90641_get_register_mcp2221());

    MLX90641_I2CInit("mcp://mcp:2221/0");

    // int state = 0;
    printf("Starting...\n");
    static uint16_t eeMLX90641[832];
    float emissivity = 1;
    uint16_t frame[834];
    // static float image[768];
    float eTa;
    // static uint16_t data[768*sizeof(float)];

    int r = MLX90641_SetRefreshRate(MLX_I2C_ADDR, 0);
    printf("Configured...%d\n", r);

    printf("refresh = %d\n", MLX90641_GetRefreshRate (MLX_I2C_ADDR));

    paramsMLX90641 mlx90641;
    MLX90641_DumpEE(MLX_I2C_ADDR, eeMLX90641);
    MLX90641_ExtractParameters(eeMLX90641, &mlx90641);

    int refresh = MLX90641_GetRefreshRate(MLX_I2C_ADDR);
    printf("EE Dumped...\n");
    printf("Refresh Rate = %d\n", refresh);

    static float mlx90641To[768];
    int counter =0;
    while(1){
        MLX90641_GetFrameData(MLX_I2C_ADDR, frame);
        eTa = MLX90641_GetTa(frame, &mlx90641)-5.0;

        printf("TA = %0.2f    -- %d\n", eTa, counter);
        counter++;
        MLX90641_CalculateTo(frame, &mlx90641, emissivity, eTa, mlx90641To);

        for(int i=0; i<12; i++){
            for(int j=0; j<16; j++){
                if(j!=19)
                    printf("%0.2f,", mlx90641To[i*16+j]);
                else
                    printf("%0.2f\n", mlx90641To[i*16+j]);
            }   
        }
        printf("\n");


    }


    /*
    uint16_t data[4];

    MLX90641_I2CInit();
    MLX90641_I2CRead(0x33, 0x800D, 4, data);

    for (int i=0; i<4; i++){
        printf("%d\n", data[i]);
       // printf("\n");
    }

    MLX90641_I2CWrite(0x33, 0x800D, 0);
    MLX90641_I2CRead(0x33, 0x800D, 4, data);

    for (int i=0; i<4; i++){
        printf("%d\n", data[i]);
       // printf("\n");
    }

    MLX90641_I2CWrite(0x33, 0x800D, 6401);
    MLX90641_I2CRead(0x33, 0x800D, 4, data);

    for (int i=0; i<4; i++){
        printf("%d\n", data[i]);
       // printf("\n");
    }

    MLX90641_I2CClose();
    */
}