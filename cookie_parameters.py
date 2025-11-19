# Cookie Parameters
# source: https://fastapi.tiangolo.com/tutorial/cookie-params/

# we can define cookie parameters that same way we define `Query` and `Path` parameters.

# Import Cookie

from typing import Annotated
from fastapi import FastAPI, Cookie, HTTPException
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

@app.get('/items')
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

# note: to declare cookies, we need to use `Cookie`, because otherwise the parameters would be interpreted as query parameters.

'''
Have in mind that, as browsers handle cookies in special ways and behind the scenes, they don't easily allow JavaScript to touch them.

If you go to the API docs UI at /docs you will be able to see the documentation for cookies for your path operations.

But even if you fill the data and click "Execute", because the docs UI works with JavaScript, the cookies won't be sent, and you will see an error message as if you didn't write any values.
'''