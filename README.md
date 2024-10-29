# Serverless HTTP Proxy

This is a serverless HTTP proxy built using FastAPI and `httpx` that can be deployed on AWS Lambda or any other serverless platform, allowing you to bypass geo-blocking without the cost of traditional proxies. It supports various HTTP methods (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `OPTIONS`) and can handle most content types. By leveraging free serverless hosting, this proxy enables low-cost, high-availability access to resources that may otherwise be regionally restricted.

## Features

- **Serverless Deployment**: Deploy on platforms like AWS Lambda, Azure Functions, or Google Cloud Functions to avoid paying for dedicated proxies.
- **Geo-Blocking Bypass**: Bypass geographical restrictions without buying dedicated proxies.
- **Full HTTP Method Support**: Supports GET, POST, PUT, DELETE, PATCH, and OPTIONS requests.
- **Custom Headers**: Forward request headers to the target URL while avoiding unnecessary headers for proxy compatibility.
- **Built with FastAPI**: FastAPI’s speed and simplicity make this solution lightweight and easy to maintain.

## Getting Started

### Requirements

- Python 3.8 or above
- FastAPI
- `httpx` for asynchronous HTTP requests
- `Mangum` for AWS Lambda compatibility with FastAPI

### Installation on AWS Lambda

As AWS Lambda doesn't have any support for installing packages from a requirements.txt file so we need to zip the required packages with the code in file `lambda_artifacts.zip`

* Install the packages in a custom directroy so we can zip them later
```bash
pip install -t deps -r requirements.txt
```
* Copy the app.py file to the `deps` folder
* Now zip the all files using this command
```bash
zip -r lambda_artifacts.zip ./*
```
* Go to AWS Lambda Dashboard and create a lmabda function in any aws region where you want.
* Make sure to enable the function url which creating lambda function.
* Click on upload from button then upload the `lambda_artifacts.zip` file to it.
* After that change the lambda handler function name to `app.handler`

### Usage
Once deployed, send HTTP requests to your proxy endpoint with the url parameter as follows:

```bash
GET https://your-lambda-url/proxy?url=https://example.com
```

```bash
curl -X POST "https://your-lambda-url/proxy?url=https://example.com" -d '{"key": "value"}' -H "Content-Type: application/json"
```

```py
import urllib.parse import quote_plus
import requests

proxy = "https://*******************mgsdoqd3a0qtutv.lambda-url.eu-central-1.on.aws/proxy"

resp = requests.get(f"{proxy}?url=https://google.com" , headers = {} , json = {})

```

### Important Notes
* CORS: The proxy does not handle CORS headers by default. Customize CORS settings as needed for your deployment.
* Serverless Limits: Be mindful of serverless platform limits, including request/response size and execution time.


