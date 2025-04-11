import utime , time
from machine import I2C, Pin
from mpu9250 import MPU9250
from ak8963 import AK8963
import motion_model
import steady_model
import unsteady_model
import staircase_model
import surface_model
from madgwick import Madgwick

mapper = {
    0 : 'Jogging' ,
    1 : 'Sitting' ,
    2 : 'Standing' ,
    3 : 'Upstairs' ,
    4 : 'Walking' ,
    5 : 'Downstairs' ,
    6 : 'Sleeping'
    }

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
I2C_ADDR = i2c.scan()
print(I2C_ADDR)
dummy = MPU9250(i2c)
ak8963 = AK8963(i2c)
sensor = MPU9250(i2c, ak8963=ak8963)
print("MPU9250 id: " + hex(sensor.whoami))
last_time = time.ticks_ms()

    
while True:
    window = []
    category = [0] * 6
    c = 0
    while(c != 10):
        X = list(sensor.gyro)+list(sensor.acceleration)
        madgwick = Madgwick(beta=0.1)
        current_time = time.ticks_ms()
        dt = time.ticks_diff(current_time, last_time) / 1000.0
        last_time = current_time
        madgwick.updateIMU(X[0], X[1], X[2], X[3], X[4], X[5], dt)
        X = madgwick.getEuler() + madgwick.getGravity() + X
        motion_score = motion_model.score(X)
        if motion_score[0] >= motion_score[1]:
            steady_score = steady_model.score(X)
            score = [0 , 0 , 0 , 0 , steady_score[0] , steady_score[1] , steady_score[2]]
        else:
            unsteady_score = unsteady_model.score(X)
            if unsteady_score[0] >= unsteady_score[1]:
                staircase_score = staircase_model.score(X)
                score = [0 , staircase_score[0] , staircase_score[1] , 0 , 0 , 0 , 0]
            else:
                surface_score = surface_model.score(X)
                score = [surface_score[0] , 0 , 0 , surface_score[1] , 0 , 0 , 0 , 0]
            
        maxval = max(score)
        for i , s in enumerate(score):
            if s == maxval:
                category[i] += 1
        utime.sleep_ms(100)
        c += 1
    maxcat = max(category)
    for i , c in enumerate(category):
        if c == maxcat:
            index = i
            break
    print(mapper.get(index) if mapper.get(index) is not None else 'nothing')
    utime.sleep_ms(1000)
