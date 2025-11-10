# Request Body
## source: https://fastapi.tiangolo.com/tutorial/body/#without-pydantic

from fastapi import FastAPI
from pydantic import BaseModel
import logfire

app = FastAPI()

logfire.configure()
logfire.instrument_fastapi(app)

# create data model and declare it as a parameter and use the model
class User(BaseModel):
    id: str
    name: str
    age: int
    about: str | None = None
    experience: str
    income: float | None = None

user_db = []

@app.post('/users/')
async def create_user(user: User):
    user_db.append(user)
    return user

@app.get('/users/')
async def get_users():
    return user_db


# use the model
class Patient(BaseModel):
    id: int
    name: str
    age: int
    description: str | None = None
    disease: str
    bed_no: str
    is_appointed: bool
    bill: float
    tax: float | None = None

@app.post('/patients/')
async def assign_patient(patient: Patient):
    # patient_dict = patient.dict() #-> it's depreciated but still we can use it in pydantic v2. instead we can use `patient.model_dump()`
    patient_dict = patient.model_dump()
    if patient.tax is not None:
        bill_with_tax = patient.bill + patient.tax
        patient_dict.update({
            "bill_with_tax": bill_with_tax
        })
    return patient_dict

# request body + path parameters
@app.put('/patients/{user_id}')
async def update_patient_information(user_id: int, patient: Patient):
    return {
        "user_id": user_id,
        #**patient.dict() # depreciated in pydantic v2, instead it is better to use `patient.model_dump()`
        #**patient.model_dump() # when we set `Patient` as optional, it will give us Attribute error and hence we can't call `patient.model_dump()`
        **patient.model_dump()
    }

# request body + path parameters + query parameters
@app.put('/users/{path_param}')
async def update_user_information(path_param: int, user: User, query_param: str | None = None):
    result = {
        "patient_id": path_param,
        **user.model_dump()
    }
    if query_param:
        result.update({
            "query_param": query_param
        })
    return result

# note: 
# # if the parameter is also declared in the path (e.g., path_param), it will be used 
# #     as a path parameter otherwise if the parameter is of singular type (e.g., int, str, float, bool) 
# #     it will be interpreted as a query parameter (e.g., query_param)
# # if the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a `request body`


#### without pydantic
## if we don't want to use Pydantic models, we can also use Body parameters, see the .. https://fastapi.tiangolo.com/tutorial/body-multiple-params/#singular-values-in-body
# Body - Multiple Parameters: https://fastapi.tiangolo.com/tutorial/body-multiple-params/
##################### Singular values in body ##################
'''
The same way there is a `Query` and `Path` to define extra data for query and path parameters,
FastAPI provides an equivalent `Body`

For instance, extending the previous model, we could decide that we want to have another key `importance`
in the same body, besides the `user` and `patient`.

if we declare it as is, because it is a singular value, FastAPI will assume that it is a query paramtere.
but we can instruct FastAPI to treat it as another body key using `Body`:
'''
from fastapi import Body
from typing import Annotated

@app.put('/singular-values-in-body/users/{u_id}')
async def update_user_info(
    u_id: int,
    user: User,
    patient: Patient,
    importance: Annotated[int, Body()]
):
    results = {
        "u_id": u_id,
        "user": user,
        "patient": patient,
        "importance": importance
    }
    return results
#
##
### Advanced use of request body declarations
##################### Body - Multiple parameters ##################
### we can also declare body parameters as optional by setting the default to `None`
##
#
from fastapi import Path

@app.put('/advanced/users/{user_id}')
async def update_user_profile(
    user_id: Annotated[int, Path(title="The ID of the user to get", ge=0, le=1000)], # ge = greater than or equal # le = less than or equal
    q: str | None = None,
    user: User | None = None
):
    results = {"user_id": user_id}
    if q:
        results.update({"q": q})
    if user:
        results.update({"user": user})
    return results


# Multiple body parameters
@app.put('/advanced/multiple-body-parameters/{user_id}')
async def update_user(user_id: int, user: User, patient: Patient):
    results = {
        "user_id": user_id,
        "user": user,
        "patient": patient
    }
    return results


### Multiple body params and query
# we can also declare additional query parameters whenever we need, additional to any body parameters.

@app.put('/multiple-body-parameters-and-query/user/{user_id}')
async def update_user_information(
    *,
    user_id: int,
    user: User,
    patient: Patient,
    importance: Annotated[int, Body(gt=0)], # `Body` also has all the same extra validation and metadata parameters as `Query`, `Path`
    q: str | None = None
):
    results = {
        "user_id": user_id,
        "user": user,
        "patient": patient,
        "importance": importance
    }
    if q:
        results.update({"q": q})
    return results

## Embed a single body parameter
'''
Let's say we only have a single `user` body parameter from a Pydantic model `User`.

By default, FastAPI will then expect its body directly.

But if we want it to expect a JSON with a key `user` and inside of it the model contents, as it does when you declare extra body parameters, you can use the special `Body` parameter `embed`:

user: User = Body(embed=True)
'''
# without embedding
@app.put('/embed-single-body-parameter-without-embed/users/{user_id}')
async def update_user_without_embed(user_id: int, patient: Patient):
    results = {
        "user_id": user_id,
        "patient": patient
    }
    return results

# with embed
@app.put('/embed-single-body-parameter-with-embed/patients/{user_id}')
async def update_user_i(
    user_id: int,
    patient: Annotated[Patient, Body(embed=True)]
):
    results = {
        "user_id": user_id,
        "patient": patient
    }
    
    return results
