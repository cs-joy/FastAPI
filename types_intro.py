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

# Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10']) # This will raise a ValidationError since there are too few dimensions, details of the input data and validation errors will be recorded in Logfire.
# Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '12', '13']) # This will raise a ValidationError since there are too few dimensions, details of the input data and validation errors will be recorded in Logfire.

##################################
# 
# Type Hints with Metadata Annotations
# Python also has a feature that allows putting additional metadata(e.g., description) in these type hints using Annotated.
# using python v3.12
from typing import Annotated

def hello_lora(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Have a good day to you, {name}"

print(hello_lora("bob"))

# 5th november 2025
## one more example
from typing import get_type_hints
def process_data(value: Annotated[int, 'This is an important integer', {'min': 0, 'max': 100}]):
    # Type checkers will treat 'value' as an 'int'
    # At runtime, you can access the metadata
    print(f"Processing value:  {value}")

class Spectre:
    id: Annotated[str, "User ID", "Unique identifier"]
    price: Annotated[float, "Product Price", {'min': 3500.678, 'max': 6025.043}]

# Accessing metadata at runtime
type_hints = get_type_hints(Spectre, include_extras=True)
print(type_hints['id'].__metadata__)
# Output: ('User ID', 'Unique identifier')
print(type_hints['price'].__metadata__)

# User cases for 'Annotated':
    # Runtime validation
    # Depenedency injection
    # Documentation and context
from typing import Annotated, get_args, get_origin

# Define types using Annotated
# We are adding constraints as metadata
StrictInt = Annotated[int, "greater_than=10", "less_than=20"]
Username = Annotated[str, "min_length=5", "max_length=20"]

def validate_data(value, type_hint):
    """
    A hypothetical 'runtime tool' validation function (e.g., a simplified FastAPI/Pydantic).
    It inspects the type hint metadata to enforce rules at runtime.
    """
    
    # Check if the type hint is an Annotated type
    if get_origin(type_hint) is Annotated:
        # Extract the base type and all metadata arguments
        # base_type_tuple[0] is the actual type (e.g., <class 'int'>)
        # metadata starts from index 1
        type_args = get_args(type_hint)
        base_type = type_args[0]
        metadata = type_args[1:]

        print(f"\nValidating value '{value}' against base type '{base_type.__name__}' with metadata: {metadata}")

        # 1. First, check the actual Python type
        if not isinstance(value, base_type):
            print(f"❌ ERROR: Expected type {base_type.__name__}, got {type(value).__name__}")
            return False

        # 2. Then, iterate over the metadata to apply custom rules
        for constraint_str in metadata:
            if isinstance(constraint_str, str) and "=" in constraint_str:
                key, val_str = constraint_str.split("=")
                
                if key == "greater_than":
                    if value <= int(val_str):
                        print(f"❌ ERROR: Value {value} is not > {val_str}")
                        return False
                
                elif key == "less_than":
                    if value >= int(val_str):
                        print(f"❌ ERROR: Value {value} is not < {val_str}")
                        return False

                elif key == "min_length":
                    if len(value) < int(val_str):
                        print(f"❌ ERROR: Length of '{value}' ({len(value)}) is not >= {val_str}")
                        return False
                
                elif key == "max_length":
                    if len(value) > int(val_str):
                        print(f"❌ ERROR: Length of '{value}' ({len(value)}) is not <= {val_str}")
                        return False
        
        print(f"✅ SUCCESS: Value '{value}' is valid.")
        return True

    else:
        # Code path for non-annotated types (e.g., just `int` or `str`)
        if isinstance(value, type_hint):
             print(f"\nValidating value '{value}' against simple type '{type_hint.__name__}'. ✅ Valid.")
             return True
        else:
             print(f"\nValidating value '{value}' against simple type '{type_hint.__name__}'. ❌ Invalid type.")
             return False


# --- Demonstration ---

print("--- Test 1: Valid StrictInt (15) ---")
validate_data(15, StrictInt)

print("\n--- Test 2: Invalid StrictInt (5) - Fails >10 check ---")
validate_data(5, StrictInt)

print("\n--- Test 3: Invalid StrictInt (String 'hello') - Fails base type check ---")
validate_data("hello", StrictInt)

print("\n--- Test 4: Valid Username ('Validator') ---")
validate_data("Validator", Username)

print("\n--- Test 5: Invalid Username ('Bob') - Fails min_length check ---")
# This is the previously problematic block, now working correctly
validate_data("Bob", Username)


########################################################
## Type hints in FastAPI
#### declare parameters with type hints and we get
            # editor support
            # type checks
#### and FastAPI uses the same declarations to:
            # define requirements: 
                # from request path parameters, query parameters, headers, bodies, dependencies and so on
            # convert data:
                # from the rquest to the required type
            # validate data:
                # coming from each request:
                    # generating automatic errors returnerd to the client when the is invalid
            #  document the APU using OpenAI:
                # which is then used by the automatic interactive documentation user interfaces

# for more to, :)
#                   Tutorial - User Guide -> https://fastapi.tiangolo.com/tutorial/
