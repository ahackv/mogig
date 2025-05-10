import time
import board
import busio
import adafruit_mhz19
import adafruit_bme280
import csv
from datetime import datetime

# Sensor Initialization
i2c = busio.I2C(board.SCL, board.SDA)
mh = adafruit_mhz19.MHZ19(board.TX, board.RX)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Sea level pressure (hPa) - adjust as needed for your location
bme280.sea_level_pressure = 1013.25

# CSV File Setup
csv_filename = 'sensor_data.csv'

def log_sensor_data():
    with open(csv_filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header if file is new
        if csvfile.tell() == 0:
            csv_writer.writerow(['Timestamp', 'CO2 (ppm)', 'Temperature (°C)', 'Pressure (hPa)', 'Altitude (m)'])

        while True:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                co2 = mh.CO2
                temperature = bme280.temperature
                pressure = bme280.pressure
                altitude = bme280.altitude

                csv_writer.writerow([timestamp, co2, temperature, pressure, altitude])
                print(f"Logged: Timestamp={timestamp}, CO2={co2} ppm, Temp={temperature:.2f}°C, Press={pressure:.2f} hPa, Alt={altitude:.2f} m")

            except Exception as e:
                print(f"Error reading sensor data: {e}")

            time.sleep(60)  # Log data every 60 seconds

if __name__ == '__main__':
    print("Starting sensor data logging. Press Ctrl+C to stop.")
    try:
        log_sensor_data()
    except KeyboardInterrupt:
        print("Logging stopped.")