import requests
from telegram import Bot

# Telegram bot API token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Telegram chat ID (your account)
CHAT_ID = 'YOUR_CHAT_ID'

# URL of your REST API endpoint to receive detection results
API_ENDPOINT = 'http://your-api-endpoint'

# Initialize Telegram bot
bot = Bot(token=BOT_TOKEN)


def send_notification(message):
    bot.send_message(chat_id=CHAT_ID, text=message)


def process_detection_results(results):
    # Process the detection results here
    # You can customize this function based on your specific logic
    # Example: Extract relevant information from the results and format a message

    message = "Detection results received:\n\n"
    for result in results:
        message += f"Object: {result['object']}, Confidence: {result['confidence']}\n"

    send_notification(message)


def receive_detection_results():
    # Make a request to your REST API endpoint to retrieve the detection results
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        results = response.json()
        process_detection_results(results)
    else:
        print("Failed to fetch detection results")


if __name__ == '__main__':
    receive_detection_results()
