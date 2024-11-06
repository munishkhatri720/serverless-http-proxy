from fastapi import FastAPI, Request , Response
from fastapi.responses import JSONResponse
import httpx  
from mangum import Mangum
from typing import Optional , Tuple , Dict , Any , List
import time


app = FastAPI(debug=True)

@app.api_route("/proxy", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy(request: Request , url : str):
    if not url:
        return Response(content="Missing 'url' query parameter", status_code=400)

    headers = {key: value for key, value in request.headers.items()
               if key.lower() not in {"host", "content-length", "accept-encoding"}}
    body = await request.body()

    async with httpx.AsyncClient() as client:
        proxy_request = client.build_request(
            method=request.method, url=url, headers=headers, content=body
        )
        proxy_response = await client.send(proxy_request)

    response_headers = {key: value for key, value in proxy_response.headers.items()
               if key.lower() not in {"content-encoding" , "content-length"}}
    return Response(content=proxy_response.content , status_code=proxy_response.status_code , headers=response_headers)

@app.api_route('/proxy/deezer/{song_id}', methods=["GET"])
async def deezer_proxy(song_id: int, request: Request) -> JSONResponse:
    try:
        start = time.time()
        
        async def format_formats(formats: List[str]) -> List[Dict[str, Any]]:
            return [{"cipher": "BF_CBC_STRIPE", "format": format} for format in formats]

        async def fetch_as_json(client: httpx.AsyncClient, request: httpx.Request) -> Optional[Dict[str, Any]]:
            resp = await client.send(request=request)
            if resp.status_code == 200:
                return resp.json()
            return None

        async def get_deezer_session(client: httpx.AsyncClient) -> Optional[str]:
            url = "https://www.deezer.com/ajax/gw-light.php?method=deezer.ping&input=3&api_version=1.0&api_token="
            request = httpx.Request(method="GET", url=url)
            result = await fetch_as_json(client, request)
            if result:
                return result.get('results', {}).get('SESSION', None)
            return result

        async def generate_license_token(client: httpx.AsyncClient, session_id: str) -> Tuple[str, str]:
            url = "https://www.deezer.com/ajax/gw-light.php?method=deezer.getUserData&input=3&api_version=1.0&api_token="
            headers = {
                'Cookie': f'sid={session_id}'
            }
            request = httpx.Request(method="GET", url=url, headers=headers)
            result = await fetch_as_json(client, request)
            if result:
                licence_token: str = result.get('results', {}).get('USER', {}).get('OPTIONS', {}).get('license_token', None)
                api_token: str = result.get('results', {}).get('checkForm', None)
                return licence_token, api_token
            return None, None

        async def generate_track_token(client: httpx.AsyncClient, session_id: str, api_token: str, song_id: str) -> Dict[str, Any]:
            url = f"https://www.deezer.com/ajax/gw-light.php?method=song.getData&input=3&api_version=1.0&api_token={api_token}"
            data = {
                'sng_id': int(song_id)
            }
            headers = {
                'Cookie': f'sid={session_id}'
            }
            request = httpx.Request(method="POST", json=data, url=url, headers=headers)
            return await fetch_as_json(client, request)

        async def get_media_url(client: httpx.AsyncClient, license_token: str, track_token: str) -> Dict[str, Any]:
            url = "https://media.deezer.com/v1/get_url"
            data = {
                'license_token': license_token,
                'media': [{"type": "FULL", "formats": await format_formats(['AAC_64', 'MP3_128'])}],
                'track_tokens': [track_token]
            }
            request = httpx.Request(method="POST", url=url, json=data)
            return await fetch_as_json(client, request)

        async with httpx.AsyncClient() as client:
            session_id = await get_deezer_session(client)
            print(f"[-] Fetched session_id in {int(time.time() - start)} sec")
            license_token, api_token = await generate_license_token(client, session_id=session_id)
            print(f"[-] Fetched licence_token and api_token in {int(time.time() - start)} sec")
            trackTokenJson = await generate_track_token(client, session_id=session_id, api_token=api_token, song_id=song_id)
            print(f"[-] Fetched track_token in {int(time.time() - start)} sec")
            mediaJson = await get_media_url(
                client,
                license_token=license_token,
                track_token=trackTokenJson['results']['TRACK_TOKEN']
            )
            print(f"[-] Fetched media url in {int(time.time() - start)} sec")
            
            response = {
                'mediaJson': mediaJson,
                'trackTokenJson': trackTokenJson,
                'time': int(time.time() - start)
            }

    except Exception as e:
        response = {
            'mediaJson': None,
            'trackTokenJson': None,
            'reason': str(e)
        }
    
    return JSONResponse(response, status_code=200)
       



handler = Mangum(app, lifespan="off")