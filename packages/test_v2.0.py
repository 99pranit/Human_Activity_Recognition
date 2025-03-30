import utime , time
from machine import I2C, Pin
from mpu9250 import MPU9250
from ak8963 import AK8963
import rf_model
from madgwick import Madgwick
import ulab.numpy as np

mapper = {
    1 : 'Jogging' ,
    2 : 'Sitting' ,
    3 : 'Standing' ,
    4 : 'Upstairs' ,
    5 : 'Walking' ,
    6 : 'Downstairs'
    }

dummy = [0] * 6
dummy2 = [0] * 12

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
I2C_ADDR = i2c.scan()
print(I2C_ADDR)
dummy = MPU9250(i2c) # this opens the bypass to access to the AK8963
ak8963 = AK8963(i2c)
sensor = MPU9250(i2c, ak8963=ak8963)
print("MPU9250 id: " + hex(sensor.whoami))
last_time = time.ticks_ms()
while True:
    X = list(sensor.gyro)+list(sensor.acceleration)
    madgwick = Madgwick(beta=0.1)
    current_time = time.ticks_ms()
    dt = time.ticks_diff(current_time, last_time) / 1000.0  # Delta time in seconds
    last_time = current_time
    madgwick.updateIMU(X[0], X[1], X[2], X[3], X[4], X[5], dt)
    X = madgwick.getEuler() + madgwick.getGravity() + X
    # Create a 1-D ulab array of samples (a sine wave in this case)
    N = 64
    sample_rate = 100  # Sampling rate in Hz
    dt = 1.0 / sample_rate
    data = [np.zeros(N) for _ in range(12)]
    
    for i in range(N):
        x = list(sensor.gyro)+list(sensor.acceleration)
        madgwick.updateIMU(X[0], X[1], X[2], X[3], X[4], X[5], dt)
        x = madgwick.getEuler() + madgwick.getGravity() + x
        data[i] = x
        time.sleep(dt)
    
    # Compute FFT: 'signal' is a vector (1-D array)
    fft_result = np.fft.fft(data)
    fft_magnitude = np.abs(fft_result)
    score = rf_model.score(X + fft_magnitude)
    maxval = max(rf_model.score(X))
    for i , s in enumerate(score):
        if s == maxval:
            print(mapper.get(i) if mapper.get(i) is not None else 'sitting')
    utime.sleep_ms(1000)


