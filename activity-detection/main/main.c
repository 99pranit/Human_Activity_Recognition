#include <stdio.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "gy91.h"
#include "predictor.h"

static const char *TAG = "ACTIVITY";
const float g = 9.80665f;

void app_main(void) {
    gy91_init();
    gy91_init_magnetometer();

    while (true) {
        float ax, ay, az, gx, gy, gz, mx, my, mz, pressure;
        gy91_read_accel(&ax, &ay, &az);
        gy91_read_gyro(&gx, &gy, &gz);
        gy91_read_magnetometer(&mx, &my, &mz);
        pressure = gy91_read_pressure();

        float roll  = atan2f(ay, az) * 180.0f / M_PI;
        float pitch = atanf(-ax / sqrtf(ay*ay + az*az)) * 180.0f / M_PI;
        float yaw   = atan2f(my, mx) * 180.0f / M_PI;

        float roll_rad  = roll  * M_PI / 180.0f;
        float pitch_rad = pitch * M_PI / 180.0f;
        float gravity_x = -g * sinf(pitch_rad);
        float gravity_y =  g * sinf(roll_rad) * cosf(pitch_rad);
        float gravity_z =  g * cosf(roll_rad) * cosf(pitch_rad);

        float input_data[16] = { roll, pitch, yaw,
                                 gravity_x, gravity_y, gravity_z,
                                 gx, gy, gz,
                                 ax, ay, az,
                                 mx, my, mz,
                                 pressure };

        int label = predict(input_data);
        const char* labels[] = {"Walking","Jogging","Downstairs","Upstairs","Standing","Sitting","Sleeping"};
        if (label >= 0 && label < 7) ESP_LOGI(TAG, "Predicted: %s", labels[label]);
        else ESP_LOGI(TAG, "Unknown activity");

        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

