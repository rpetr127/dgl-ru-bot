import os

BOT_TOKEN = os.getenv('TOKEN')
if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

PROCESS = "web"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 5000))


WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_PORT = 443
WEBHOOK_URL = f'{WEBHOOK_PORT}{WEBHOOK_PATH}'
