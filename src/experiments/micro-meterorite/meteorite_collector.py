'''
Control a servo for a micrometeorite collector based on altitude.
Runs on a Raspberry Pi and uses an SG90 servo and BME280 sensor.
'''
import time
import board
import busio
import adafruit_bme280
import RPi.GPIO as GPIO

# --- Configuration Constants ---
SERVO_PIN = 17  # GPIO pin connected to the servo signal wire (using BCM numbering)

# Altitude thresholds (in meters)
ALTITUDE_OPEN = 20000  # Altitude to open the collector
ALTITUDE_CLOSE = 18000 # Altitude to close the collector (on descent)

# Servo angles (0-180 degrees). Adjust these for your specific servo and mechanism.
# Typically, SG90: 0 degrees might be 2.5% duty cycle, 180 degrees 12.5%.
# We'll use these as placeholders.
SERVO_OPEN_ANGLE = 90  # Angle for the "open" position
SERVO_CLOSED_ANGLE = 0 # Angle for the "closed" position

# BME280 Configuration
SEA_LEVEL_PRESSURE = 1013.25  # Standard sea level pressure in hPa. Adjust if necessary.

# --- Global Variables ---
collector_is_open = False
pwm = None

# --- Sensor Initialization ---
def initialize_bme280():
    '''Initializes the BME280 sensor.'''
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        bme280.sea_level_pressure = SEA_LEVEL_PRESSURE
        print("BME280 sensor initialized.")
        return bme280
    except Exception as e:
        print(f"Error initializing BME280: {e}")
        return None

# --- Servo Setup and Control ---
def setup_servo():
    '''Sets up GPIO for servo control.'''
    global pwm
    try:
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        GPIO.setwarnings(False) # Disable warnings for GPIO already in use if re-running
        pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM frequency
        pwm.start(0)  # Start PWM with 0% duty cycle (off)
        print(f"Servo on GPIO {SERVO_PIN} initialized.")
        # Set to initial closed position
        set_servo_angle(SERVO_CLOSED_ANGLE)
        time.sleep(1)
        pwm.ChangeDutyCycle(0) # Stop sending signal to servo to prevent jitter
    except Exception as e:
        print(f"Error setting up servo: {e}")
        GPIO.cleanup() # Clean up GPIO on error
        exit()

def angle_to_duty_cycle(angle):
    '''Converts an angle (0-180) to a PWM duty cycle (2.5-12.5 for SG90).'''
    # SG90 typically uses 1ms pulse for 0 deg and 2ms pulse for 180 deg.
    # PWM frequency is 50Hz, so period is 20ms.
    # Duty cycle = (pulse_width_ms / 20ms) * 100
    # Pulse width = 1ms + (angle / 180) * 1ms  => (for 0-180 mapped to 1-2ms)
    # More generally, for a typical 2.5% to 12.5% range for 0-180:
    # duty_cycle = 2.5 + (angle / 180.0) * 10.0
    # Clamp angle to 0-180
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    return 2.5 + (angle / 180.0) * 10.0

def set_servo_angle(angle):
    '''Sets the servo to a specific angle.'''
    global pwm
    if pwm is None:
        print("Servo not initialized.")
        return
    duty = angle_to_duty_cycle(angle)
    print(f"Setting servo to angle: {angle} deg, duty cycle: {duty:.2f}%")
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Allow time for the servo to move
    pwm.ChangeDutyCycle(0) # Stop sending signal to servo to prevent jitter and save power

def open_collector():
    '''Opens the micrometeorite collector.'''
    global collector_is_open
    print("Attempting to open collector...")
    set_servo_angle(SERVO_OPEN_ANGLE)
    collector_is_open = True
    print("Collector OPENED.")

def close_collector():
    '''Closes the micrometeorite collector.'''
    global collector_is_open
    print("Attempting to close collector...")
    set_servo_angle(SERVO_CLOSED_ANGLE)
    collector_is_open = False
    print("Collector CLOSED.")

# --- Main Logic ---
def main():
    global collector_is_open
    bme280 = initialize_bme280()
    if not bme280:
        print("Exiting due to BME280 sensor initialization failure.")
        return

    setup_servo()

    print(f"Collector script started. Will open at {ALTITUDE_OPEN}m and close at {ALTITUDE_CLOSE}m.")
    print(f"Initial state: Collector is {'Open' if collector_is_open else 'Closed'}")

    try:
        while True:
            try:
                current_altitude = bme280.altitude
                if current_altitude is None:
                    print("Failed to read altitude. Skipping this cycle.")
                    time.sleep(10) # Wait longer if sensor read fails
                    continue
                
                print(f"Current Altitude: {current_altitude:.2f} m")

                if not collector_is_open and current_altitude > ALTITUDE_OPEN:
                    print(f"Altitude ({current_altitude:.2f}m) is above open threshold ({ALTITUDE_OPEN}m).")
                    open_collector()
                elif collector_is_open and current_altitude < ALTITUDE_CLOSE:
                    print(f"Altitude ({current_altitude:.2f}m) is below close threshold ({ALTITUDE_CLOSE}m).")
                    close_collector()
                else:
                    status = "Open" if collector_is_open else "Closed"
                    print(f"Collector remains {status}. Altitude: {current_altitude:.2f}m")

            except Exception as e:
                print(f"Error in main loop: {e}")
            
            time.sleep(30)  # Check altitude every 30 seconds

    except KeyboardInterrupt:
        print("Script interrupted by user.")
    finally:
        print("Cleaning up GPIO...")
        if pwm:
            pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete. Exiting.")

if __name__ == '__main__':
    main()
