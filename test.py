import requests
from rich import print
from urllib.parse import quote_plus


proxy = "http://**********:8000/proxy"

r = requests.post(f'{proxy}?url={quote_plus("https://www.deezer.com/ajax/gw-light.php?method=deezer.ping&input=3&api_version=1.0&api_token=")}')



data = r.json()

session_id = data['results']['SESSION']

headers = {
    'Cookie' : f'sid={session_id}'
}


r = requests.get(f'{proxy}?url={quote_plus("https://www.deezer.com/ajax/gw-light.php?method=deezer.getUserData&input=3&api_version=1.0&api_token=")}' , headers=headers)

license_token = r.json().get('results').get('USER').get('OPTIONS').get('license_token')

api_token : str = r.json().get('results').get('checkForm')


data = {'sng_id' : 2307207795}

url = f"https://www.deezer.com/ajax/gw-light.php?method=song.getData&input=3&api_version=1.0&api_token={api_token}"
r = requests.post(f'{proxy}?url={quote_plus(url)}' , json=data , headers=headers)


track_token = r.json().get('results')['TRACK_TOKEN']


def format_formats(formats):
    return [{"cipher": "BF_CBC_STRIPE", "format": format} for format in formats]


data = {
    'license_token': license_token,
    'media': [{"type": "FULL", "formats": format_formats(['AAC_64' , 'MP3_128'])}],
    'track_tokens': [track_token]
}



url = quote_plus("https://media.deezer.com/v1/get_url")

r = requests.post(f'{proxy}?url={url}' , json=data)



print(r.text)





