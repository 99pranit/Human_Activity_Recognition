import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from ak8963 import AK8963
import rf_model

mapper = {
    0 : 'walking upstairs' ,
    1 : 'walking downstairs' ,
    2 : 'walking' ,
    3 : 'sitting' ,
    4 : 'standing' ,
    5 : 'jogging'
    }

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
I2C_ADDR = i2c.scan()
print(I2C_ADDR)
dummy = MPU9250(i2c) # this opens the bypass to access to the AK8963
ak8963 = AK8963(i2c)
sensor = MPU9250(i2c, ak8963=ak8963)
print("MPU9250 id: " + hex(sensor.whoami))
while True:
    #print(sensor.acceleration)
    #print(sensor.gyro)
    X = list(sensor.acceleration)+list(sensor.gyro)
    score = rf_model.score(X)
    maxval = max(rf_model.score(X))
    for i , s in enumerate(score):
        if s == maxval:
            print(mapper.get(i) if mapper.get(i) is not None else 'undetectable')
    utime.sleep_ms(1000)


