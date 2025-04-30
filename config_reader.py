import configparser
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

config = configparser.ConfigParser()
config.read('./victoria_secret/keys.ini')

SERVICE_ACCOUNT_FILE = "victoria_secret/client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("drive", "v3", credentials=creds)

def proxy_config():

    proxy_ips = config.get('proxy', 'ip').split(',')
    login = config.get('proxy', 'login')
    password = config.get('proxy', 'password')

    # Используем счетчик для отслеживания текущего индекса прокси
    if 'proxy_index' not in proxy_config.__dict__:
        proxy_config.proxy_index = 0
    else:
        proxy_config.proxy_index = (proxy_config.proxy_index + 1) % len(proxy_ips)

    current_proxy = proxy_ips[proxy_config.proxy_index]
    proxy_url = f'http://{login}:{password}@{current_proxy}'

    proxy_configuration = {
        'http': proxy_url,
        'https': proxy_url
    }

    return proxy_configuration
gpt_tokens = config.get('gpt', 'keys').split(',')
print(len(gpt_tokens), 'tokens')

telegram_token = config.get('telegram', 'key')
admins_ids = [int(i) for i in config.get('telegram', 'admins_ids').split(',')]
