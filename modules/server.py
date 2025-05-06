import network
import socket
import ujson
import utime, time
from machine import I2C, Pin
import gc

wifi_ssid = 'OnePlus 10R 5G'
wifi_password = '34567890'

# Define HTML template with continuous data fetching
html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Activity Recognition System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Activity Recognition</h1>
        <div id="status">Status: Initializing...</div>
        <div id="activity">Activity: Unknown</div>
        <div id="last-update">Last update: Never</div>
        <div id="auto-refresh">
            <label>
                <input type="checkbox" id="toggle-refresh" checked>
                Auto-refresh
            </label>
            <span id="refresh-interval">(2 seconds)</span>
        </div>
    </div>
    <script>
        let autoRefresh = true;
        let refreshTimer;
        
        function updateTimestamp() {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            document.getElementById('last-update').textContent = 'Last update: ' + timeString;
        }
        
        function getActivity() {
            document.getElementById('status').textContent = 'Status: Fetching data...';
            
            fetch('/activity')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').textContent = 'Status: ' + data.status;
                    document.getElementById('activity').textContent = 'Activity: ' + data.activity;
                    updateTimestamp();
                })
                .catch(error => {
                    document.getElementById('status').textContent = 'Status: Error fetching data';
                    console.error('Error:', error);
                });
        }
        
        function startAutoRefresh() {
            getActivity(); // Get data immediately
            
            // Set up interval for continuous updates
            refreshTimer = setInterval(() => {
                if (autoRefresh) {
                    getActivity();
                }
            }, 3000); // Refresh every 2 seconds
        }
        
        // Setup toggle for auto-refresh
        document.getElementById('toggle-refresh').addEventListener('change', function() {
            autoRefresh = this.checked;
            document.getElementById('status').textContent = autoRefresh ? 
                'Status: Auto-refresh enabled' : 
                'Status: Auto-refresh disabled';
        });
        
        // Start the auto-refresh when page loads
        window.onload = startAutoRefresh;
    </script>
</body>
</html>
"""

css_styles = """
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}
.container {
    max-width: 600px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
h1 {
    color: #333;
    text-align: center;
}
#status, #activity, #last-update {
    margin: 15px 0;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 4px;
}
#activity {
    font-size: 1.2em;
    font-weight: bold;
    text-align: center;
}
#auto-refresh {
    margin-top: 20px;
    text-align: center;
}
#refresh-interval {
    color: #666;
    font-size: 0.9em;
}
"""

# Global state variable
device_state = False

# Wi-Fi connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    max_attempts = 5  # Number of retry attempts
    for attempt in range(max_attempts):
        try:
            wlan.connect(wifi_ssid , wifi_password)
            start_time = time.time()
            while not wlan.isconnected():
                if time.time() - start_time > 10:  # 10-second timeout per attempt
                    raise OSError("Connection timeout")
                time.sleep(0.1)
            display.screen(wlan.ifconfig()[0]).show_once()
            print("Connected to WiFi:", wlan.ifconfig())
            return True
        except OSError as e:
            print(f"WiFi connection attempt {attempt+1} failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
            else:
                print("Failed to connect to WiFi after multiple attempts.")
                return False
    return False

try:
    # Initialize I2C and sensors
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
    i2c_devices = i2c.scan()
    print("I2C devices found:", i2c_devices)

    # Only import these modules if I2C devices are found
    if i2c_devices:
        try:
            from mpu9250 import MPU9250
            from ak8963 import AK8963
            import motion_model, steady_model, unsteady_model, staircase_model, surface_model
            from madgwick import Madgwick
            import display
            
            dummy = MPU9250(i2c)
            ak8963 = AK8963(i2c)
            sensor = MPU9250(i2c, ak8963=ak8963)
            print("MPU9250 id:", hex(sensor.whoami))
            sensors_initialized = True
        except Exception as e:
            print("Sensor initialization error:", e)
            sensors_initialized = False
    else:
        print("No I2C devices found.")
        sensors_initialized = False

    # Button setup
    pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
    last_button_state = pin.value()
    last_time = time.ticks_ms()
    
except Exception as e:
    print("Hardware initialization error:", e)
    sensors_initialized = False

# Activity mapping
mapper = {
    0: 'Walking',
    1: 'Jogging',
    2: 'Downstairs',
    3: 'Upstairs',
    4: 'Sitting',
    5: 'Standing',
    6: 'Sleeping'
}

# We'll use a buffer to store recent predictions for smoothing
prediction_buffer = []
buffer_size = 3  # Store last 3 predictions for smoothing

def get_prediction():
    global device_state, last_button_state, last_time, prediction_buffer
    
    if not sensors_initialized:
        return "Sensor Error"
    
    # Check button state
    current_button_state = pin.value()
    
    if last_button_state == 1 and current_button_state == 0:
        # Button pressed (falling edge)
        utime.sleep_ms(500)
        if pin.value() == 0:
            device_state = not device_state
            if not device_state:
                display.screen("Device OFF").show_once()
            else:
                display.screen("Device ON").show_once()
    
    last_button_state = current_button_state

    if not device_state:
        display.screen("System is OFF").show_once()
        utime.sleep_ms(100) 
        return "Device OFF"
    
    category = [0] * 7
    c = 0
    samples_to_collect = 30 
    
    while c < samples_to_collect:
        try:
            X = list(sensor.gyro) + list(sensor.acceleration) + list(sensor.magnetic) + [sensor.temperature]
            madgwick = Madgwick(beta=0.1)
            current_time = time.ticks_ms()
            dt = time.ticks_diff(current_time, last_time) / 1000.0
            last_time = current_time
            madgwick.updateIMU(X[0], X[1], X[2], X[3], X[4], X[5], dt)
            X = madgwick.getEuler() + madgwick.getGravity() + X
            
            # Model scoring logic
            motion_score = motion_model.score(X)
            if motion_score[0] >= motion_score[1]:
                steady_score = steady_model.score(X)
                score = [0, 0, 0, 0, steady_score[0], steady_score[1], steady_score[2]]
            else:
                unsteady_score = unsteady_model.score(X)
                if unsteady_score[0] <= unsteady_score[1]:
                    staircase_score = staircase_model.score(X)
                    score = [0, 0, staircase_score[0], staircase_score[1], 0, 0, 0]
                else:
                    surface_score = surface_model.score(X)
                    score = [surface_score[0], surface_score[1], 0, 0, 0, 0, 0]
            
            # Find highest score
            maxval = max(score)
            for i, s in enumerate(score):
                if s == maxval:
                    category[i] += 1
                    
            utime.sleep_ms(50)  # Reduced sleep time
            c += 1
            
        except Exception as e:
            print("Prediction error:", e)
            return "Sensor Error"
    
    # Determine most frequent category
    maxcat = max(category)
    index = 0
    for i, c in enumerate(category):
        if c == maxcat:
            index = i
            break
        
    
    activity = mapper.get(index , 'Unknown')
    
    # Add to prediction buffer for smoothing
    #prediction_buffer.append(activity)
    #if len(prediction_buffer) > buffer_size:
       # prediction_buffer.pop(0)
    
    # Simple smoothing - return most common prediction in buffer
    #if prediction_buffer:
        #activity_counts = {}
        #for a in prediction_buffer:
            #if a in activity_counts:
                #activity_counts[a] += 1
            #else:
                #activity_counts[a] = 1
        
        # Find most common activity in buffer
        #max_count = 0
        #smoothed_activity = activity
        #for a, count in activity_counts.items():
            #if count > max_count:
               # max_count = count
                #smoothed_activity = a
        
        #activity = smoothed_activity
    
    print("Detected activity:", activity)
    
    # Display the result
    display.screen(activity).show_once()
    return activity

def start_server():
    try:
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print('Listening on', addr)

        while True:
            try:
                cl, addr = s.accept()
                request = cl.recv(1024).decode('utf-8')
                request_line = request.split('\r\n')[0]
                print("Request:", request_line)

                if 'GET / ' in request_line or 'GET /index.html' in request_line:
                    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
                    cl.sendall(html_template)

                elif 'GET /style.css' in request_line:
                    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n')
                    cl.sendall(css_styles)

                elif 'GET /activity' in request_line:
                    activity = get_prediction()
                    result = {'status': 'success', 'activity': activity}
                    response = ujson.dumps(result)
                    cl.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
                    cl.send(response)

                else:
                    cl.send('HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot Found')

            except Exception as e:
                print("Client handling error:", e)
            finally:
                cl.close()
                # Run garbage collection to free memory
                gc.collect()
    
    except Exception as e:
        print("Server error:", e)

# Main execution
def main():
    if connect_wifi():
        start_server()
    else:
        print("Failed to connect to WiFi, cannot start server.")

if __name__ == "__main__":
    main()




