from fastapi import FastAPI, Request , Response
from fastapi.responses import JSONResponse
import httpx  
from mangum import Mangum
from deezer import get_deezer_sesssion , generate_track_token , generate_license_token , get_media_url

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

@app.api_route('/proxy/deezer/{song_id}' , methods=["GET"])
async def deezer_proxy(song_id : int , request : Request) -> JSONResponse:
    try:
        session_id = await get_deezer_sesssion()
        if not session_id:
            session_id = await get_deezer_sesssion()
        license_token , api_token = await generate_license_token(session_id=session_id)    
        if not license_token and api_token:
            session_id = await get_deezer_sesssion()
            license_token , api_token = await generate_license_token(session_id=session_id)  

        trackTokenJson = await generate_track_token(session_id=session_id , api_token=api_token , song_id=song_id)
        if not trackTokenJson:
            session_id = await get_deezer_sesssion()
            trackTokenJson = await generate_track_token(session_id=session_id , api_token=api_token , song_id=song_id)
        mediaJson = await get_media_url(license_token=license_token , track_token=trackTokenJson['results']['TRACK_TOKEN']) 
        response = response = {
            'mediaJson' : mediaJson,
            'trackTokenJson' : trackTokenJson
        }      
    except Exception as e:
        response = {
            'mediaJson' : None,
            'trackTokenJson' : None
        }
    return JSONResponse(response , status_code=200)        



handler = Mangum(app, lifespan="off")