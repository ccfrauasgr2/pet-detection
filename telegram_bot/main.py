import os
import requests
import base64


def send_telegram_notification(detection_results):
    """
    notifies user about detection results via Telegram Bot
    """

    # Retrieve the bot token and chat ID from environment variables
    bot_token = base64.b64decode(os.environ['TELEGRAM_BOT_TOKEN']).decode("utf-8")
    group_chat_id = base64.b64decode(os.environ['TELEGRAM_CHAT_ID']).decode("utf-8")

    caption = "Detected following pet(s):"
    for det in detection_results["detections"]:

        bid = det["BID"]
        pet_type =  det["type"]
        accuracy = det["accuracy"]
    
        temp = f"\nBID: {bid} - Type: {pet_type} - Accuracy: {accuracy}"
        caption += temp

    img = base64.b64decode(detection_results["picture"])

    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={group_chat_id}&caption={caption}'
    response = requests.post(url, files={'photo': img})
    
    if response.status_code == 200:
        print('Notification sent successfully!')
    else:
        print('Failed to send notification.')



os.environ['TELEGRAM_BOT_TOKEN'] = "NTg3MDMxOTU2ODpBQUhhN1RIU3hJSllJTU1tUGNrNUlIZV9qVVRHYmNpRHBkOA=="
os.environ['TELEGRAM_CHAT_ID'] = "OTg4MzM2MzA2"

with open("img/sample_img.png", "rb") as image_file:
    encoded_img = base64.b64encode(image_file.read())

detection_results = {
  "picture": f"{encoded_img}",
  "date": "28.05.2023",
  "time": "10:01:23",
  "detections": [
    {
      "type": "dog",
      "accuracy": 0.91,
      "BID": 1
    },
    {
      "type": "cat",
      "accuracy": 0.79,
      "BID": 2
    }
  ]
}

# Example usage
send_telegram_notification(detection_results)
