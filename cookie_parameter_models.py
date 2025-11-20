# Cookie Parameter Models

# source: https://fastapi.tiangolo.com/tutorial/cookie-param-models/


# if we have a group of cookies that are related, we can create a pydantic model to declare them.
# this would allow us to re-use the model in the multiple places and also to declare validations and metadata for all the parameters at once

# This same technique applies to `Query`, `Cookie` and `Header`

from fastapi import FastAPI, Cookie
from pydantic import BaseModel
from typing import Annotated
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


class Cookies(BaseModel):
    session_id: str
    facebook_tracker: str | None = None
    google_tracker: str | None = None


@app.get('/cookie-parameters-model/')
async def cookie_params_models(cookies: Annotated[Cookies, Cookie()]):
    return cookies

# Have in mind that, as browser handle cookies in special ways and behind the scenes, they don't easily asllow JavaScript to touch them.

# If we go to the API docs UI at /docs we will be able to see tge documentation for cookies for your path operations.

# But even if we fill the data and click `Execute`, because the docs UI works with JavaScript, the cookies won't be sent, and we will see an error message as if we don't write any values


'''
Forbid Extra Cookies
'''
# In some special use cases (probably not very common), we might want to restrict the cookies that we want to receive.

# our API now has the power to control its own `cookie consent`.

# we can use Pydantic's model configuration to `forbid` any `extra` fields.

class CookiesModel(BaseModel):
    model_config = {"extra": "forbid"}

    session_id: str
    facebook_tracker: str | None = None
    google_tracker: str | None = None

@app.get('/forbid-extra-cookies/')
async def forbid_extra_cookies(cookies: Annotated[CookiesModel, Cookie()]):
    return cookies


# If a client tries to send some extra cookies, they will receive an error response.
# Poor cookie banners with all their effort to get our consent for the API to reject it. :) #coffee time :)
# For example, 
#               If the client tries to send `santa-tracker` cookie with a value of `good-list-please`, the client will receive an error
#               response telling them that the `santa_tracker` cookie is not allowed.
'''
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
'''

# Summary: we can use Pydantic models to declare `cookies` in FastAPI