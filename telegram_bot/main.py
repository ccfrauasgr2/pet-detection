import os
import telegram
import base64
import asyncio


async def send_telegram_notification(detection_results):
    """
    notifies user about detection results via TNB

    Notification = Image + Caption
    """

    # Retrieve the bot token and group chat ID from environment variables
    # NOTE: Remove base64.b64decode().decode("utf-8") when integrating this code into API code, since Kubernetes does base64 decoding automatically for environment variables specified in Kubernetes Secret
    bot_token = base64.b64decode(os.environ['TELEGRAM_BOT_TOKEN']).decode("utf-8")
    group_chat_id = "-" + base64.b64decode(os.environ['TELEGRAM_CHAT_ID']).decode("utf-8")

    # Get image for notification
    img = base64.b64decode(detection_results["picture"])

    # Create caption for notification
    caption = "Detected following pet(s):"
    for det in detection_results["detections"]:
        bid = det["bid"]
        pet_type =  det["type"]
        accuracy = det["accuracy"]
        temp = f"\nBID: {bid} - Type: {pet_type} - Accuracy: {accuracy}"
        caption += temp

    # Initialize the TNB
    bot = telegram.Bot(token=bot_token)

    # Send detection results to the TNB
    await bot.send_photo(chat_id=group_chat_id, photo=img, caption=caption)


# EXAMPLE USAGE
# FOR TESTING ON LOCAL PC ONLY
# NOT FOR TESTING ON CLUSTER

# Initialize environment variables
os.environ['TELEGRAM_BOT_TOKEN'] = "<Base64 encoded string of the bot token>"
os.environ['TELEGRAM_CHAT_ID'] = "<Base64 encoded string of the group chat id>"

# Sample image encoded as base64-string
with open("img/sample_img.png", "rb") as image_file:
    encoded_img = base64.b64encode(image_file.read())

# Sample detection results
detection_results = {
  "picture": encoded_img,
  "date": "2023-05-28",
  "time": "10:01:23",
  "detections": [
    {
      "type": "Dog",
      "accuracy": 0.91,
      "bid": 1
    },
    {
      "type": "Cat",
      "accuracy": 0.79,
      "bid": 2
    }
  ]
}

# Run method to test TNB
asyncio.run(send_telegram_notification(detection_results))
