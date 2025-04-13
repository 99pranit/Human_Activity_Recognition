import utime , time
from machine import I2C, Pin
from mpu9250 import MPU9250
from ak8963 import AK8963
from madgwick import Madgwick


i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
I2C_ADDR = i2c.scan()
print(I2C_ADDR)
dummy = MPU9250(i2c) # this opens the bypass to access to the AK8963
ak8963 = AK8963(i2c)
sensor = MPU9250(i2c, ak8963=ak8963)
print("MPU9250 id: " + hex(sensor.whoami))
n = 4
#filename = 'upstarirs_' + str(n)
#filename = 'downstairs_' + str(n)

# filename = 'walking_' + str(n)
#filename = 'jogging_' + str(n)

#filename = 'standing_' + str(n)
#filename = 'sitting_' + str(n)
filename = 'sleeping_' + str(n)

data = []
count = 0
last_time = time.ticks_ms()
data.append(['attitude.roll', 'attitude.pitch', 'attitude.yaw', 'gravity.x',
             'gravity.y', 'gravity.z', 'rotationRate.x', 'rotationRate.y',
             'rotationRate.z', 'userAcceleration.x', 'userAcceleration.y',
             'userAcceleration.z', 'magnetic.x', 'magnetic.y',
             'magnetic.z' , 'temperature'])
while count != 2200:
    X = list(sensor.gyro)+list(sensor.acceleration) + list(sensor.magnetic) + [sensor.temperature]
    madgwick = Madgwick(beta=0.1)
    current_time = time.ticks_ms()
    dt = time.ticks_diff(current_time, last_time) / 1000.0  # Delta time in seconds
    last_time = current_time
    madgwick.updateIMU(X[0], X[1], X[2], X[3], X[4], X[5], dt)
    X = madgwick.getEuler() + madgwick.getGravity() + X
    data.append(X)
    utime.sleep_ms(100)
    count += 1
    
with open(filename + '.txt', mode='w') as file:
    for row in data:
        file.write(str(row).strip('[').strip(']') + '\n')
                   
print(f'File {filename} has been created.')


