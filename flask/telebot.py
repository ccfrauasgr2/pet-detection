import os
import telegram # requires "pip install python-telegram-bot"
import base64


async def send_telegram_notification(detection_results):
    """
    notifies user about detection results via a TNB

    Notification = Image + Caption
    """

    # Retrieve the bot token and group chat ID from environment variables
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    group_chat_id = "-" + os.environ['TELEGRAM_CHAT_ID']

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