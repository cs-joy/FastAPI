# Path Parameters and Numeric Validations
# source: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/

'''
In the same way we can declare more validations and metadata for query parameters
 with `Query`, we can declare the same type of validations and metadaya for path parameters with `Path`.
'''


from fastapi import FastAPI, Path, Query
from typing import Annotated
import logfire
from pydantic import BaseModel

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

class Patient(BaseModel):
    id: int
    name: str
    age: int
    disease: str


@app.get('/patient/{patient_id}')
async def view_patient_info(
    patient_id: Annotated[int, Path(title="The ID of the patient to get")],
    patient_query: Annotated[str | None, Query(alias="patient-query")] = None,
):
    results = {"patient_id": patient_id}
    if patient_query:
        results.update({"patient_query": patient_query})
    return results

### Delcare metadata
# to declare a `title` metadata value for the path parameter `patient_id` you can type:
# patient_id: Annotated[int, Path(title="The ID of the patient to get")]

# note: A path parameter is always required even if you declared it with `None`
#----------------

### Order the parameters as we need
# source: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#order-the-parameters-as-you-need
#-> python v3.8+ - non-Annotated

# make `q` is required: q: str
# make `q` is optional:> q: str | None = None
@app.get('/order-the-parameters-as-we-need/{product_id}')
async def view_product_information(q: str, product_id: int = Path(title="The ID of the product to get")):
    results = {"product_id": product_id}
    if q:
        results.update({"q": q})
    return results

# note this is probably not as important or necessary if we use `Annotated`

# keyword arguments - kwargs
@app.get('/k-wargs/{item_id}')
async def read_item(*, item_id: int = Path(title= "The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# note: better with `Annotated`

# --------------------------------------
# Number validations: greater than or equal
# With `Query` and `Path` (and others you'll see later) you can declare number constraints (e.g., ge=1)
@app.get('/number-validations/{item_id}')
async def number_validations(item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validations: greater than and less than or equal
# gt -> greater than
# ge -> greater than or equal
# lt -> less than
# le -> less than or equal

@app.get('/num-validations/{mark}')
async def number_validation(mark: Annotated[int, Path(title="subject marks", gt=0, lt=100)], q: str):
    results = {"mark": mark}
    if q:
        results.update({"q": q})
    return results


# Number validations: floats, greater than and less than
### number validations also work for `float` values.
@app.get('/float-number/{number}')
async def float_number(
    *, 
    number: Annotated[int, Path(title="The number of the item to get", ge=0, le=1000)], 
    q: str,
    size: Annotated[float, Query(gt=0, lt=0.5)],
):
    results = {"number": number}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results



# Recap
'''
With `Query` and `Path` we can declare metadata and string validations in the same ways as with
Query Parameters and String Validations:-> https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

## numeric validations
# gt - greater than
# ge - greater than or equal
# lt - less than
# le - less than or equal
'''


