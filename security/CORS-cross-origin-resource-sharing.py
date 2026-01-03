# CORS (Cross-Origin Resource Sharing
# source: https://fastapi.tiangolo.com/tutorial/cors/

'''
CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend running in a browser
Javascript code that communicates with a backend, and the backend is in a different "origin" than the frontend.

# Origin
An origin is the combination of protocol (http, https), domain (myapp.com, localhost, localhost.tiangolo.com), and
port (80, 443, 8080).

So, all these are different origins:
- http://localhost
- https://localhost
- http://localhost:8080

Even if they are all in `localhost`, they use different protocols or ports, so they are a different "origins".

# Steps
So, let's say we have a frontend running in our browser at `http://localhost:8080` and its 
JavaScript is trying to communicate with a backend running at `http://localhost` (becuase we don't specify a port, the browser will assume the default port is `80`).

Then the browser will send an HTTP `OPTIONS` request to the `:80`-backend, and if the backend sends the approprate headers
authorizing the communication from this different origin (`http://localhost:8080`) the n`:8080`-broswer will let the JavaScript
in the frontend send its request to the `:80`-backend.

To achieve this, the `:80`-backend must have a list of "allowed origins".

In this case, the list would have to include `http://localhost:8080` for the `:8080`-frontend to work correctly.

# Wildcards
It's also possible to declare the list as "*" (a "wildcard") to sat that all are allowed.
But that will only allow certain types of communication, excluding everything that involves credentials:
- Cookies
- Authorization headers
like those used with Bearer Tokens, etc.

So, for everything to work correctly, it's better to specify explcitly the allowed origins.

# Use `CORSMiddleware`
We can configure it in our FastAPI application using the `CORSMiddleware`.
- Import `CORSMiddleware`
- Create a list of allowed origins (as strings).
- Add it as a "middleware" to our FastAPI application.

We can also specify whether our backend allows.
- Credentials (Authorizatio headers, Cookies, etc)
- Specify HTTP methods (`POST`, `PUT`) or all of them with the wildcard "*"
- Specific HTTP headers or all of them with the wildcard "*"
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
async def main():
    return {
        "message": "Hello FastAPI!"
    }


'''
The default parameters used by the `CORSMiddleware` implementation are restrictive by default, 
so we'll need to explicitly enable particular origins, methods, or headers, in order for browsers 
to be permitted to use them in a Cross-Domain context.

The following arguments are supported:
- `allow_origins` - list of origins that should be permitted to make cross-origin request. E.g.
    ['https://example.org', 'https://www.example.org']. We can use ['*'] to allow any origin.
- `allow_origin_regex` - A regex string to match against origins that should be permitted to 
    make cross-origin requests. E.g., 'https://.*\example\.org'.
- `allow_methods` - list of HTTP methods that should be allowed for cross-origin requests. Default
    ['GET']. We can user ['*'] to allow all standard methods.
- `allow_headers` - list of HTTP request headers that should be supported for cross-origin requests.
    Default []. We can user ['*'] to allow all headers. The `Accept`, `Accept-Language`, `Content-Language`,
    and `Content-Type` headers are always allowed for "simple CORS requests: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests"
- `allow_credentials` - indicate that cookies should be supported for cross-origin requests. Default to `False`
    None of `allow_origins`, `allow_methods` and `allow_headers` can be set ['*'] if `allow_credentials` is set to `True`. 
    All of them must be "explicitly specified: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#credentialed_requests_and_wildcards"
- `expose_headers` - indicate any response headers that should be made accessible to the browser. Default to []

The middleware responds to two particular types of HTTP request...

# CORS preflight requests:
These are any `OPTIONS` request with `Origin` and `Access-Control-Request-Method` headers.
In this case the middleware will intercept the incoming request and response with appropriate CORS headers,
and either a `200` or `400` response for informational purposes.

# Simple requests
Any request with an `Origin` header. In this case the middleware will pass the request throug as normal,
but will include appropriate CORS headers on the response.
'''

# More info:
# For more info about CORS, check the "Mozila CORS documentation: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS"


