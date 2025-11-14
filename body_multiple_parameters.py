# Body - Multiple Parameters
# source: https://fastapi.tiangolo.com/tutorial/body-multiple-params/

# advanched uses of -> request of body declarations


from typing import Annotated, Literal
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path, Body
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)


## Mix `Path`, `Query` and body parameteres

# we can declare body parameters as optional, by setting the default to `None`.

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put('/body-multiple-parameters/{item_id}')
async def body_multiple_parameters(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=100)],
    q: str | None = None, # query parameter as optional
    item: Item | None = None, # body as optional
):
    results = {
        "item_id": item_id
    }
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# Multiple Body parameters
'''
In the previous example, the path operations would expect a JSON 
body with the attributes of an `Item` like:
{
    "name": "Mouse",
    "description": "Wireless mouse - Logitech",
    "price": 555,
    "tax": 15
}
But we can also declare multple body parameters, e.g., `item` and `user`:
'''

# let's create two different model
class Surah(BaseModel):
    surah_no: int
    name: str
    total_ayah: int

class Recitator(BaseModel):
    username: str
    age: int

@app.put('/al-quran/{surah_no}')
async def update_item(
    surah_no: Annotated[int, Path(title="number of the Surah", gt=0, le=114)],
    surah: Surah,
    recitator: Recitator
):
    profile_of_surah = {
        "surah_no": surah_no,
        "surah": surah,
        "recitator": recitator
    }
    return profile_of_surah

class Revealed(BaseModel):
    place: str


## Singular values in body and Multiple body params and query
@app.put('/singular-valuse-in-body/{surah_no}')
async def singular_values_in_body(
    surah_no: int,
    surah: Surah,
    recitator: Recitator,
    revealed: Revealed,
    importance: Annotated[int, Body()],
    search_at: str | None = None # Query params
):
    profile = {
        "surah_no": surah_no,
        "surah": surah,
        "recitator": recitator,
        "revealed": revealed,
        "importance": importance
    }
    if search_at:
        profile.update({"search_at": search_at})
    return profile

# Embed a single body parameter
@app.put('/embed/{surah_no}')
async def embed(surah_no: int, surah: Annotated[Surah, Body(embed=True)]):
    profile = {"surah_no": surah_no, "surah": surah}
    return profile
