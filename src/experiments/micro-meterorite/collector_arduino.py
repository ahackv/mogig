# collector_arduino.py
# Python script for Arduino (CircuitPython) to control a micro-meteorite collector

import time
import board
import busio
import adafruit_bme280
import pwmio
from adafruit_motor import servo

# --- Configuration Constants ---
# IMPORTANT: Adjust these pin definitions for your specific Arduino board and wiring!
# Example pins (these are common but may vary):
SERVO_PIN = board.D9  # Digital pin connected to the servo signal wire
SCL_PIN = board.SCL   # I2C SCL (Clock) pin for BME280
SDA_PIN = board.SDA   # I2C SDA (Data) pin for BME280

# Altitude thresholds (in meters)
ALTITUDE_OPEN = 20000  # Altitude to open the collector
ALTITUDE_CLOSE = 18000 # Altitude to close the collector (on descent)

# Servo angles (0-180 degrees).
# Adjust these for your SD90 servo and collector door mechanism.
SERVO_OPEN_ANGLE = 90  # Angle for the "open" position
SERVO_CLOSED_ANGLE = 0 # Angle for the "closed" position

# BME280 Configuration
SEA_LEVEL_PRESSURE = 1013.25  # Standard sea level pressure in hPa. Adjust if necessary.

# --- Global Variables ---
collector_is_open = False
collector_servo = None  # Will be initialized as a servo.Servo object
bme280_sensor = None    # Will be initialized as an Adafruit_BME280_I2C object

# --- Sensor and Servo Initialization ---
def initialize_bme280():
    """Initializes the BME280 sensor."""
    global bme280_sensor
    try:
        i2c = busio.I2C(SCL_PIN, SDA_PIN)
        bme280_sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        bme280_sensor.sea_level_pressure = SEA_LEVEL_PRESSURE
        print("BME280 sensor initialized successfully.")
        # Print some initial readings
        print(f"Initial Temperature: {bme280_sensor.temperature:.2f} C")
        print(f"Initial Pressure: {bme280_sensor.pressure:.2f} hPa")
        print(f"Initial Altitude (approx): {bme280_sensor.altitude:.2f} m")
        return True
    except Exception as e:
        print(f"Error initializing BME280: {e}")
        print("Please check I2C wiring and sensor address.")
        bme280_sensor = None
        return False

def setup_servo():
    """Initializes the SD90 servo."""
    global collector_servo
    try:
        # Create a PWMOut object on the servo pin
        # Typical hobby servos run at 50 Hz
        pwm_out = pwmio.PWMOut(SERVO_PIN, duty_cycle=0, frequency=50)
        # Create a Servo object. Min_pulse and max_pulse might need adjustment for SD90.
        # Default values are often 500-2500 microseconds for 0-180 degrees.
        collector_servo = servo.Servo(pwm_out) # You can add min_pulse and max_pulse here if needed
        collector_servo.angle = SERVO_CLOSED_ANGLE # Start with collector closed
        print(f"Servo initialized on pin {str(SERVO_PIN)}. Initial angle: {SERVO_CLOSED_ANGLE} degrees.")
        return True
    except Exception as e:
        print(f"Error initializing servo: {e}")
        print(f"Ensure pin {str(SERVO_PIN)} supports PWM and is correctly connected.")
        collector_servo = None
        return False

# --- Servo Control Functions ---
def open_collector_door():
    """Opens the collector door."""
    global collector_is_open, collector_servo
    if collector_servo:
        try:
            collector_servo.angle = SERVO_OPEN_ANGLE
            collector_is_open = True
            print(f"Collector door opened. Servo angle: {SERVO_OPEN_ANGLE} degrees.")
        except Exception as e:
            print(f"Error setting servo to open: {e}")
    else:
        print("Servo not initialized. Cannot open collector door.")

def close_collector_door():
    """Closes the collector door."""
    global collector_is_open, collector_servo
    if collector_servo:
        try:
            collector_servo.angle = SERVO_CLOSED_ANGLE
            collector_is_open = False
            print(f"Collector door closed. Servo angle: {SERVO_CLOSED_ANGLE} degrees.")
        except Exception as e:
            print(f"Error setting servo to close: {e}")
    else:
        print("Servo not initialized. Cannot close collector door.")

# --- Main Logic ---
def main_loop():
    global collector_is_open, bme280_sensor

    # Initialize components
    if not initialize_bme280():
        print("BME280 sensor critical failure. Check wiring and try resetting. Will retry initialization.")
        # Loop will attempt re-initialization later
    
    if not setup_servo():
        print("Servo critical failure. Check wiring and try resetting. Will retry initialization.")
        # Loop will attempt re-initialization later
    else:
        # Ensure collector starts closed if servo initialized correctly
        close_collector_door()


    print(f"Collector script started. Door will open above {ALTITUDE_OPEN}m and close below {ALTITUDE_CLOSE}m.")
    print(f"Initial state: Collector door is {'Open' if collector_is_open else 'Closed'}")

    while True:
        # Attempt to re-initialize if components are not ready
        if not bme280_sensor:
            print("Attempting to re-initialize BME280 sensor...")
            time.sleep(5) # Wait before retrying
            if not initialize_bme280():
                print("BME280 re-initialization failed. Will try again later.")
                time.sleep(25) # Longer wait if still failing
                continue # Skip to next loop iteration
        
        if not collector_servo:
            print("Attempting to re-initialize servo...")
            time.sleep(5) # Wait before retrying
            if not setup_servo():
                print("Servo re-initialization failed. Will try again later.")
                time.sleep(25) # Longer wait if still failing
                continue # Skip to next loop iteration
            else:
                # Ensure door is closed after servo re-initialization
                close_collector_door()


        try:
            current_altitude = bme280_sensor.altitude
            if current_altitude is None:
                print("Failed to read altitude (got None). Skipping this cycle.")
                time.sleep(10) # Wait longer if sensor read fails
                continue
            
            print(f"Current Altitude: {current_altitude:.2f} m")

            if not collector_is_open and current_altitude > ALTITUDE_OPEN:
                print(f"Altitude ({current_altitude:.2f}m) is above open threshold ({ALTITUDE_OPEN}m). Opening door.")
                open_collector_door()
            elif collector_is_open and current_altitude < ALTITUDE_CLOSE:
                print(f"Altitude ({current_altitude:.2f}m) is below close threshold ({ALTITUDE_CLOSE}m). Closing door.")
                close_collector_door()
            else:
                status = "Open" if collector_is_open else "Closed"
                print(f"Collector door remains {status}. Altitude: {current_altitude:.2f}m")

        except RuntimeError as e:
            print(f"Runtime error in main loop (often I2C issue): {e}")
            print("Attempting to recover. Will re-initialize BME280 if it happens again soon.")
            # Simple recovery: wait and hope it resolves. If it persists, re-init might be needed.
            time.sleep(5)
            # Potentially reset BME280 sensor object to trigger re-initialization
            bme280_sensor = None 
        except Exception as e:
            print(f"An unexpected error occurred in main loop: {e}")
            # For other errors, try to re-initialize everything after a delay
            print("Attempting to re-initialize all components after unexpected error.")
            bme280_sensor = None
            collector_servo = None
            time.sleep(10) # Wait before comprehensive re-initialization attempt
        
        time.sleep(15)  # Check altitude and conditions every 15 seconds

if __name__ == "__main__":
    # This structure is common in standard Python but less so in basic CircuitPython
    # scripts which often run code directly. However, it's good practice.
    # For many CircuitPython boards, the code in 'code.py' runs automatically.
    # If you save this as code.py on your board, main_loop() will be called.
    main_loop()
