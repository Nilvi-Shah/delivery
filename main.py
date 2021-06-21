import requests
import json
import time
from boltiot import Bolt
import conf
mybolt = Bolt(conf.bolt_api_key, conf.device_id)
response = mybolt.serialBegin('9600')
def get_sensor_value_from_pin():
    """Returns the sensor value. Returns -999 if requefist fails"""
    try:
        response = mybolt.digitalRead('0')

        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successfull")
            print("This is the response->", data)
            return -999
        sensor_value = int(data["value"])
        return sensor_value
    except Exception as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999
def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False
while True:
    mybolt.digitalWrite('1','LOW')
    sensor_value = get_sensor_value_from_pin()
    print("The current sensor value is:", sensor_value)

    if sensor_value==1:
       print("Your Order has been delivered")
       message="Your order is delivered"
       telegram_status=send_telegram_message(message)
       print("This is the telegram status:",telegram_status)

       t_end=time.time()+60
       while time.time()<t_end:
        sensor_value=get_sensor_value_from_pin()
        print("HI")
        if sensor_value==0:
           mybolt.digitalWrite('1','HIGH')
           print("some one removed your parcel")
           message="Someome is taking your package"
           telegram_status=send_telegram_message(message)
        elif sensor_value==1:
           print("You order is in the box you can take it after 6 hours we will inform you")

        time.sleep(10)
       print("You can take your order from box")
       message="You can Now remove your order from box"
       telegram_status=send_telegram_message(message)
    time.sleep(10)
