import os
import requests
import base64

# TODO: Define a method for sending notifications and run this method inside any PUT or POST request

def send_telegram_notification(detection_results):
    """
    notifies user about detection results via Telegram Bot
    """

    # Retrieve the bot token and chat ID from environment variables
    bot_token = base64.b64decode(os.environ['TELEGRAM_BOT_TOKEN']).decode("utf-8")
    group_chat_id = base64.b64decode(os.environ['TELEGRAM_CHAT_ID']).decode("utf-8")

    caption = detection_results
    img = open("img/sample_img.png", 'rb')

    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={group_chat_id}&caption={caption}'
    response = requests.post(url, files={'photo': img})
    
    if response.status_code == 200:
        print('Notification sent successfully!')
    else:
        print('Failed to send notification.')

# Example usage
send_telegram_notification('Detection results')
