# Serverless HTTP Proxy

This is a serverless HTTP proxy built using FastAPI and `httpx` that can be deployed on AWS Lambda or any other serverless platform, allowing you to bypass geo-blocking without the cost of traditional proxies. It supports various HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS) and can handle most content types. By leveraging free serverless hosting, this proxy enables low-cost, high-availability access to resources that may otherwise be regionally restricted.

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

### Installation

Install the required libraries:

```bash
pip install fastapi httpx mangum
```
