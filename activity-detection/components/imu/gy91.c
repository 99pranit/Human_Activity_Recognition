#include "gy91.h"
#include "esp_log.h"
#include "driver/i2c.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "GY91";
static i2c_port_t i2c_port = I2C_PORT;

// I2C Write Function
static esp_err_t i2c_write_byte(uint8_t addr, uint8_t reg, uint8_t data) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg, true);
    i2c_master_write_byte(cmd, data, true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(i2c_port, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    return ret;
}

// I2C Read Function (Multiple Bytes)
esp_err_t i2c_read_bytes(uint8_t addr, uint8_t reg, uint8_t *data, uint8_t len) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, reg, true);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_READ, true);
    i2c_master_read(cmd, data, len, I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(i2c_port, cmd, 1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    return ret;
}

// I2C Read Function (Word)
int16_t i2c_read_word(uint8_t addr, uint8_t reg) {
    uint8_t data[2];
    if (i2c_read_bytes(addr, reg, data, 2) != ESP_OK) {
        ESP_LOGE(TAG, "I2C read error from 0x%X", addr);
        return -1;
    }
    return (int16_t)((data[0] << 8) | data[1]);
}

// Initialize GY-91 Sensors
void gy91_init() {
    i2c_config_t config = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA,
        .scl_io_num = I2C_MASTER_SCL,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ
    };
    i2c_param_config(i2c_port, &config);
    i2c_driver_install(i2c_port, config.mode, 0, 0, 0);

    if (i2c_write_byte(MPU9250_ADDR, PWR_MGMT_1, 0x00) == ESP_OK) {
        ESP_LOGI(TAG, "MPU9250 initialized.");
    } else {
        ESP_LOGE(TAG, "Failed to initialize MPU9250.");
    }

    gy91_init_magnetometer();
    gy91_init_pressure();
}

// Initialize Magnetometer (AK8963)
void gy91_init_magnetometer() {
    i2c_write_byte(MPU9250_ADDR, 0x37, 0x02);
    vTaskDelay(pdMS_TO_TICKS(10));

    i2c_write_byte(AK8963_ADDR, AK8963_CNTL1, 0x16);
    vTaskDelay(pdMS_TO_TICKS(10));

    uint8_t mode;
    i2c_read_bytes(AK8963_ADDR, AK8963_CNTL1, &mode, 1);
    ESP_LOGI(TAG, "Magnetometer Mode: %02X", mode);
}

// Initialize BMP280
void gy91_init_pressure() {
    i2c_write_byte(BMP280_ADDR, BMP280_CTRL_MEAS, 0x27);
    i2c_write_byte(BMP280_ADDR, BMP280_CONFIG, 0xA0);
    vTaskDelay(pdMS_TO_TICKS(10));
}

// Read Accelerometer Data
void gy91_read_accel(float *ax, float *ay, float *az) {
    *ax = i2c_read_word(MPU9250_ADDR, ACCEL_XOUT_H) / 16384.0;
    *ay = i2c_read_word(MPU9250_ADDR, ACCEL_XOUT_H + 2) / 16384.0;
    *az = i2c_read_word(MPU9250_ADDR, ACCEL_XOUT_H + 4) / 16384.0;
}

// Read Gyroscope Data
void gy91_read_gyro(float *gx, float *gy, float *gz) {
    *gx = i2c_read_word(MPU9250_ADDR, GYRO_XOUT_H) / 131.0;
    *gy = i2c_read_word(MPU9250_ADDR, GYRO_XOUT_H + 2) / 131.0;
    *gz = i2c_read_word(MPU9250_ADDR, GYRO_XOUT_H + 4) / 131.0;
}

// Read Magnetometer Data
void gy91_read_magnetometer(float *mx, float *my, float *mz) {
    uint8_t data[6];

    if (i2c_read_bytes(AK8963_ADDR, AK8963_XOUT_L, data, 6) != ESP_OK) {
        ESP_LOGE(TAG, "Failed to read magnetometer data");
        return;
    }

    int16_t raw_x = (int16_t)(data[1] << 8 | data[0]);
    int16_t raw_y = (int16_t)(data[3] << 8 | data[2]);
    int16_t raw_z = (int16_t)(data[5] << 8 | data[4]);

    *mx = raw_x * 0.15;
    *my = raw_y * 0.15;
    *mz = raw_z * 0.15;
}

// Read Pressure Data (BMP280)
float gy91_read_pressure() {
    uint8_t data[3];
    if (i2c_read_bytes(BMP280_ADDR, BMP280_PRESS_MSB, data, 3) != ESP_OK) {
        ESP_LOGE(TAG, "Failed to read pressure");
        return -1;
    }
    int32_t raw_pressure = ((int32_t)data[4] << 7) | ((int32_t)data[0] << 7) | (data[7] >> 0);
    return raw_pressure /256.0;
}