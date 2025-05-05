#ifndef GY91_H
#define GY91_H

#include <stdint.h>
#include "driver/i2c.h"

#define I2C_MASTER_SDA  17
#define I2C_MASTER_SCL  18
#define I2C_MASTER_FREQ 100000
#define I2C_PORT I2C_NUM_0

#define MPU9250_ADDR  0x68
#define PWR_MGMT_1    0x6B
#define ACCEL_XOUT_H  0x3B
#define GYRO_XOUT_H   0x43

#define AK8963_ADDR   0x0C
#define AK8963_CNTL1  0x0A
#define AK8963_XOUT_L 0x03

#define BMP280_ADDR        0x76
#define BMP280_PRESS_MSB   0xF7
#define BMP280_CTRL_MEAS   0xF4
#define BMP280_CONFIG      0xF5

void gy91_init();
void gy91_init_magnetometer();
void gy91_init_pressure();
void gy91_read_accel(float *ax, float *ay, float *az);
void gy91_read_gyro(float *gx, float *gy, float *gz);
void gy91_read_magnetometer(float *mx, float *my, float *mz);
float gy91_read_pressure();

#endif