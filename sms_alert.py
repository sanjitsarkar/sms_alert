import conf  # imports the conf.py file
# imports the sms and Bolt module from the boltiot library
from boltiot import Sms, Bolt
import json
import time  # imports the json and time module

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
while True:
    print("Reading sensor value")
    response = mybolt.digitalRead('0')  # reads the sensor value
    data = json.loads(response)
    print(data)
    print("Sensor value is: " + str(data["value"]))
    try:
        # Converts the data type from str to int
        sensor_value = int(data["value"])
        if sensor_value > 0:  # checks the condition,if user touches the sensor, it becomes 1 from 0
            mybolt.digitalWrite('1', 'HIGH')  # Enables the buzzer
            print("Making request to Twilio to send a SMS")
            # send sms,number should be provided instead of xxxxxxxxxx
            response = sms.send_sms(
                "Alert!!! Someone is in danger. Track this number: 8253993139 ")
            print("Response received from Twilio is: " + str(sensor_value))
            print("Status of SMS at Twilio is :" + str(response.status))
            time.sleep(10)  # wait for 10 seconds
            mybolt.digitalWrite('1', 'LOW')  # turns off the buzzer
        else:
            mybolt.digitalWrite('1', 'LOW')

    except Exception as e:
        print("Error occured: Below are the details")
        print(e)
    time.sleep(1)
