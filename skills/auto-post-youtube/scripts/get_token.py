# Usage: python get_token.py client_secret.json
# Opens the browser once to sign in to the YouTube channel, then writes the 3 OAuth values to .env (never printed).
import json, sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(sys.argv[1], ['https://www.googleapis.com/auth/youtube.force-ssl'])
creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
Path('.env').open('a', encoding='utf-8').write(
    f'YOUTUBE_OAUTH_CLIENT_ID={creds.client_id}\n'
    f'YOUTUBE_OAUTH_CLIENT_SECRET={creds.client_secret}\n'
    f'YOUTUBE_OAUTH_REFRESH_TOKEN={creds.refresh_token}\n')
print('saved to .env')
