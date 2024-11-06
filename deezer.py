import httpx
from typing import Optional , Tuple , Dict , Any , List


def format_formats(formats : List[str]) -> List[Dict[str ,Any]]:
    return [{"cipher": "BF_CBC_STRIPE", "format": format} for format in formats]


async def fetch_as_json(request : httpx.Request):
    async with httpx.AsyncClient() as client:
        resp = await client.send(request=request)
        if resp.status_code == 200:
            return resp.json()
        return None

async def get_deezer_sesssion() -> Optional[str]:
    url = "https://www.deezer.com/ajax/gw-light.php?method=deezer.ping&input=3&api_version=1.0&api_token="  
    request = httpx.Request(method="GET" , url=url)
    result = await fetch_as_json(request)
    if result:
        return result.get('results', {}).get('SESSION', None)
    return result

async def generate_license_token(session_id : str) -> Tuple[str , str]:
    url = "https://www.deezer.com/ajax/gw-light.php?method=deezer.getUserData&input=3&api_version=1.0&api_token="
    headers = {
        'Cookie' : f'sid={session_id}'
    }
    request = httpx.Request(method="GET" , url=url , headers=headers)
    result = await fetch_as_json(request)
    if result:
        licence_token : str = result.get('results' , {}).get('USER' , {}).get('OPTIONS' , {}).get('license_token' , None)
        api_token : str = result.get('results' , {}).get('checkForm' , None)
        return licence_token , api_token
    return None , None

async def generate_track_token(session_id : str , api_token : str , song_id : str) -> Dict[str , Any]:
    url = f"https://www.deezer.com/ajax/gw-light.php?method=song.getData&input=3&api_version=1.0&api_token={api_token}"
    data = {
        'sng_id' : int(song_id)
    }
    headers = {
        'Cookie' : f'sid={session_id}'
    }
    request = httpx.Request(method="POST" , json=data , url=url  , headers=headers)
    return await fetch_as_json(request)
      

async def get_media_url(license_token : str , track_token : str) -> Dict[str , Any]:
    url = "https://media.deezer.com/v1/get_url"
    data = {
    'license_token': license_token,
    'media': [{"type": "FULL", "formats": format_formats(['AAC_64' , 'MP3_128'])}],
    'track_tokens': [track_token]
}
    request = httpx.Request(method="POST" , url=url , json=data)
    return await fetch_as_json(request)
    