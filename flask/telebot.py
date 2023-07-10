import os
import telegram # requires "pip install python-telegram-bot"
import base64
import asyncio


async def send_telegram_notification(detection_results):
    """
    notifies user about detection results via a TNB

    Notification = Image + Caption
    """

    # Retrieve the bot token and group chat ID from environment variables
    bot_token = base64.b64decode(os.environ['TELEGRAM_BOT_TOKEN']).decode("utf-8")
    group_chat_id = "-" + base64.b64decode(os.environ['TELEGRAM_CHAT_ID']).decode("utf-8")

    # Get image for notification
    img = base64.b64decode(detection_results["picture"])

    # Create caption for notification
    caption = "Detected following pet(s):"
    for det in detection_results["detections"]:
        bid = det["BID"]
        pet_type =  det["type"]
        accuracy = det["accuracy"]
        temp = f"\nBID: {bid} - Type: {pet_type} - Accuracy: {accuracy}"
        caption += temp

    # Initialize the TNB
    bot = telegram.Bot(token=bot_token)

    # Send detection results to the TNB
    await bot.send_photo(chat_id=group_chat_id, photo=img, caption=caption)

"""
# EXAMPLE USAGE

# Initialize environment variables
os.environ['TELEGRAM_BOT_TOKEN'] = "NTg3MDMxOTU2ODpBQUhhN1RIU3hJSllJTU1tUGNrNUlIZV9qVVRHYmNpRHBkOA=="
os.environ['TELEGRAM_CHAT_ID'] = "OTg4MzM2MzA2"

# Sample image encoded as base64-string
with open("img/sample_img.png", "rb") as image_file:
    encoded_img = base64.b64encode(image_file.read())

# Sample detection results
detection_results = {
  "picture": encoded_img,
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

# Run method to test TNB
asyncio.run(send_telegram_notification(detection_results))
"""