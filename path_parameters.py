# DATA CONVERSION
## Data Validation


from fastapi import FastAPI

app = FastAPI()


@app.get('/students/{student_id}') # path parameter = {student_id}
async def view_student_profile(student_id: int):
    return {
        "student_id": student_id
    }

# type declaration
@app.get('/students/{student_name}/{student_id}/{tution_fee}/{is_paid}')
async def view_student_tution_fee(student_name: str, student_id: int, tution_fee: float, is_paid: bool):
    return {
        "student_name": student_name,
        "student_id": student_id,
        "tution_fee": tution_fee,
        "is_paid": is_paid
    }


# # # # # # # # # # # # # # Order Matters # # # # # # # # # #
@app.get('/users/alis')
async def read_user_alis():
    return {
        "user_id": "the current user"
    }

@app.get('/users/{user_id}')
async def read_user(user_id: str):
    return {
        "user_id": user_id
    }

# if you declare `/users/{user_id}` before `/users/alis`, the path for `/users/{user_id}` would
# match also for `/users/me`, "thinking" that it's receiving a parameter `user_id` with a value of `me`

# Similarly, you can not redefine a path operation:
@app.get('/verses/{verses_no}')
async def get_verse(verses_no: int):
    return ["Ayatul Qursi", "..."]

@app.get('/verses/{verses_no}')
async def get_verses2(verses_no: int):
    return ["...", "Ayatul Qursi"]

# the first one will always be used since the path matches first.

# # # # # # # # # # # Predefined values # # # # # # # # # # # #
'''
if we have a path operation that receives a path parameter, but we want the possible valid path parameters values to be predefined,
we can use a standard Python `Enum`
'''
from enum import Enum

class Model(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get('/models/{model_name}')
async def get_model(model_name: Model):
    if model_name is Model.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }
    if model_name.value == 'lenet':
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }
    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }

# visit http://localhost:8000/docs

####### Working with Python enumerations
# the value of the path parameter will be an enumeration member.
# get the enumeration value using `model_name.value`, or in general, `you_enum_member.value`:
# even, we could also access the value `lenet` with `ModelName.lenet.value`

# Path converter
# `/files/{files_path:path}`
@app.get('/files/{file_path:path}')
async def view_chain(file_path: str):
    return {
        "file_path": file_path
    }