import network
import urequests
import time
from machine import ADC

# Wi-Fi credentials
SSID = "XIME-WIFi_STUDENTS"
PASSWORD = "Xime@560100"

# ThingSpeak details
API_KEY = "8ACSISXIGTZTPP4O"
URL = "https://api.thingspeak.com/update?api_key=8ACSISXIGTZTPP4O&field1=" + API_KEY

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
print("Connected:", wlan.ifconfig())

# Sensor setup
wind_speed_sensor = ADC(26)  # Wind speed analog input
wind_direction_sensor = ADC(27)  # Wind direction analog input

def read_wind_speed():
    raw = wind_speed_sensor.read_u16()
    return round((raw / 65535) * 100, 2)  # Scale to 0–100 km/h

def read_wind_direction():
    raw = wind_direction_sensor.read_u16()
    return round((raw / 65535) * 360, 2)  # Scale to 0–360 degrees

while True:
    # Simulated data
    temp = 25 + (time.time() % 10)  # Dummy temp value
    wind_speed = read_wind_speed()
    wind_direction = read_wind_direction()

    # Send to ThingSpeak
    try:
        full_url = f"{URL}&field1={temp}&field2={wind_speed}&field3={wind_direction}"
        response = urequests.get(full_url)
        print("Data sent:", response.text)
        response.close()
    except Exception as e:
        print("Error sending data:", e)

    time.sleep(20)  # ThingSpeak limit = 15 sec minimum

