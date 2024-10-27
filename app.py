from fastapi import FastAPI, Request , Response
import httpx  
from mangum import Mangum

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
    

handler = Mangum(app, lifespan="off")