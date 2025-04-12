import math

class Madgwick:
    def __init__(self, beta=0.1, q0=1.0, q1=0.0, q2=0.0, q3=0.0):
        self.beta = beta
        self.q0 = q0
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

    def updateIMU(self, gx, gy, gz, ax, ay, az, dt):
        # Convert gyroscope degrees/s to radians/s
        gx = math.radians(gx)
        gy = math.radians(gy)
        gz = math.radians(gz)

        q0, q1, q2, q3 = self.q0, self.q1, self.q2, self.q3

        # Normalize accelerometer measurement
        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if norm == 0:
            return  # avoid division by zero
        ax /= norm
        ay /= norm
        az /= norm

        # Auxiliary variables to avoid repeated arithmetic
        _2q0 = 2.0 * q0
        _2q1 = 2.0 * q1
        _2q2 = 2.0 * q2
        _2q3 = 2.0 * q3

        # Gradient descent algorithm corrective step
        # (This is a simplified IMU-only version of Madgwick’s algorithm.)
        f1 = _2q1 * q3 - _2q0 * q2 - ax
        f2 = _2q0 * q1 + _2q2 * q3 - ay
        f3 = 1.0 - _2q1 * q1 - _2q2 * q2 - az

        s0 = -_2q2 * f1 + _2q1 * f3
        s1 = _2q3 * f1 + _2q0 * f3 - 4.0 * q1 * f2
        s2 = -_2q0 * f1 + _2q3 * f2 - 4.0 * q2 * f3
        s3 = _2q1 * f1 + _2q2 * f2

        norm_s = math.sqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3)
        if norm_s == 0:
            return
        s0 /= norm_s
        s1 /= norm_s
        s2 /= norm_s
        s3 /= norm_s

        # Compute rate of change of quaternion
        qDot0 = 0.5 * (-q1 * gx - q2 * gy - q3 * gz) - self.beta * s0
        qDot1 = 0.5 * (q0 * gx + q2 * gz - q3 * gy) - self.beta * s1
        qDot2 = 0.5 * (q0 * gy - q1 * gz + q3 * gx) - self.beta * s2
        qDot3 = 0.5 * (q0 * gz + q1 * gy - q2 * gx) - self.beta * s3

        # Integrate to yield quaternion
        q0 += qDot0 * dt
        q1 += qDot1 * dt
        q2 += qDot2 * dt
        q3 += qDot3 * dt

        # Normalize quaternion
        norm_q = math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
        q0 /= norm_q
        q1 /= norm_q
        q2 /= norm_q
        q3 /= norm_q

        self.q0, self.q1, self.q2, self.q3 = q0, q1, q2, q3

    def getEuler(self):
        # Convert current quaternion to Euler angles (roll, pitch, yaw)
        q0, q1, q2, q3 = self.q0, self.q1, self.q2, self.q3
        sinr_cosp = 2.0 * (q0 * q1 + q2 * q3)
        cosr_cosp = 1.0 - 2.0 * (q1 * q1 + q2 * q2)
        roll = math.degrees(math.atan2(sinr_cosp, cosr_cosp))

        sinp = 2.0 * (q0 * q2 - q3 * q1)
        if abs(sinp) >= 1:
            pitch = math.degrees(math.copysign(math.pi / 2, sinp))
        else:
            pitch = math.degrees(math.asin(sinp))

        siny_cosp = 2.0 * (q0 * q3 + q1 * q2)
        cosy_cosp = 1.0 - 2.0 * (q2 * q2 + q3 * q3)
        yaw = math.degrees(math.atan2(siny_cosp, cosy_cosp))
        return [roll, pitch, yaw]

    def getGravity(self):
        # Compute the gravity vector in the sensor frame from the quaternion
        q0, q1, q2, q3 = self.q0, self.q1, self.q2, self.q3
        # In a perfect system, if global gravity is [0, 0, g] (with g normalized to 1),
        # then the gravity vector in sensor frame becomes:
        g_x = 2.0 * (q1 * q3 - q0 * q2)
        g_y = 2.0 * (q0 * q1 + q2 * q3)
        g_z = q0 * q0 - q1 * q1 - q2 * q2 + q3 * q3
        return [g_x, g_y, g_z]
