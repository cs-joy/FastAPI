# we used python v3.9

# v1
'''
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()

    return full_name

print(get_full_name("john", "doe"))
'''

# v2
# best solution
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()

    return full_name

print(get_full_name("john", "doe"))

# v3
'''
def get_full_name(first_name="john", last_name="doe"):
    full_name = first_name.title() + " " + last_name.title()

    return full_name
'''


###################################
def get_name_with_age(name: str, age: int):
    #name_with_age = name + " is this old: " + age # error
    name_with_age = name + " is this old: " + str(age)

    return name_with_age

print(get_name_with_age("john", 21))


##### Declaring Types #####
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_e

########### Generic Types with parameters
'''
-> dict
-> list
-> set
-> tuple

There are some data structures that can contain other values, like dict, list, set and tuple. And the internal values can have their own type too.

These types that have internal types are called "generic" types. And it's possible to declare them, even with their internal types.

To declare those types and the internal types, you can use the standard Python module typing. It exists specifically to support these type hints.
'''
# List
    # let's define a variable to be a `list` of `str`
def library(books: list[str]):
    for book in books:
        print(book)
'''
def library(books: list):
    for book in books:
        print(book.)
'''

# Tuple and Set
def pharmacy(medicine: tuple[int, str, int, bool, float], tablet: set[bytes]): # tuple[serial_no, medicine_name, product_code, is_expired, price]
    return medicine, tablet

# Dict
def garden(trees: dict[str, bool]):
    for tree_name, tree_price in trees.items():
        print(tree_name)
        print(tree_price)

# Union
    # You can declare that a variable can be any of several types, for example, an int or a str.
# python 3.8+
from typing import Union
def addition(num: Union[int, float]): #  this means that 'num' could be an `int` or a `str`.
    return num

'''
for python3.10+
def union_types(num: int | float):
    return num
'''

######## Possibly `None` ###########
    # you can declare that a value could have a type, like `bool` but that is could also be `None`.
# python v3.10+
'''
def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
'''
# python v3.8+
from typing import Optional
def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("hello lora")
# python v3.8+ - alternative
'''
from typing import Union
def say_hi(name: Union[str, None] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("hello, lora!")
#################################################
# Note: If you are using a Python version below 3.10, here's a tip from my very subjective point of view:

🚨 Avoid using Optional[SomeType]
Instead ✨ use Union[SomeType, None] ✨.

Both are equivalent and underneath they are the same, but 
I would recommend Union instead of Optional because the word 
"optional" would seem to imply that the value is optional, 
and it actually means "it can be None", even if it's not 
optional and is still required.
'''
from typing import Optional
def say_hii(name: Optional[str]):
    print(f"Hey {name}!")
# say_hii() # throws an error!


## Generic Types
# List
# Tuple
# Set
# Dict
# Union
# Optional
# ...and others

# Classes as types
class Student:
    def __init__(self, name: str):
        self.name = name
    

def get_person_name(one_student: Student):
    return one_student.name


## Pydantic models
# examples: https://docs.pydantic.dev/latest/#why-use-pydantic
from datetime import datetime
from pydantic import BaseModel, PositiveInt

class User(BaseModel):
    id: int # required
    name: str = 'John Doe' # optional
    signup_ts: Optional[datetime] = None # 
    tastes: dict[str, PositiveInt] # required

external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22', # The input here is an ISO 8601 formatted datetime, but Pydantic will convert it to a datetime object.
    'tastes': {
        'wine': 9,
        b'cheese': 7, # The key here is bytes, but Pydantic will take care of coercing it to a string.
        'cabbage': 1 # Similarly, Pydantic will coerce the string '1' to the integer 1.
    },
}

user = User(**external_data) # We create instance of User by passing our external data to User as keyword arguments.

print('\nPydantic Examples')

print(user.id)
print(user.signup_ts)

print(user.model_dump()) # We can convert the model to a dictionary with model_dump().

### Validation Error
print('\nValidation Error Analysis')
from pydantic import ValidationError

new_external_data = {'id': 'not an int', 'tastes': {}} # The input data is wrong here — id is not a valid integer, and signup_ts is missing.

try:
    User(**new_external_data) # Trying to instantiate User will raise a ValidationError with a list of errors.
except ValidationError as e:
    print(e.errors())

################
print('\n')
# from here i used `python v3.12` - new venv-> fastAPI_venv_3_12
print('Pydantic Models')
'''
Pydantic Logfire<https://pydantic.dev/logfire> is an application monitoring tool that is as simple to use and powerful as Pydantic itself.

Logfire integrates with many popular Python libraries including FastAPI, OpenAI and Pydantic
 itself, so you can use Logfire to monitor Pydantic validations and understand why some inputs fail validation:
'''
print('Monitoring Pydantic with Logfire')
from datetime import datetime
import logfire
from pydantic import BaseModel

logfire.configure()
logfire.instrument_pydantic()

class Delivery(BaseModel):
    timestamp: datetime
    dimensions: tuple[int, int]

# this will record details of a successful validation to logfire
m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
print(m.dimensions)

Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10']) # This will raise a ValidationError since there are too few dimensions, details of the input data and validation errors will be recorded in Logfire.