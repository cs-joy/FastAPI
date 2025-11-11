## Query Parameters and String Validations
# source: https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

# fastapi allow us to declare additional information and validation for your parameters

from fastapi import FastAPI
from pydantic import BaseModel
import logfire

app = FastAPI()
logfire.configure()
logfire.instrument_fastapi(app)

@app.get('/items/')
async def read_items(q: str | None = None):
    results = {
       "items": [
           {
               "item_id": "Foo"
           },
           {
               "item_id": "Bar"
           }
       ]
    }

    if q:
        results.update({"q": q})
    return results

# fastapi will know that the value of `q` is not required because of the default value = None
# Having `str | None` will allow our editor to give us better support and detect errors.

### Additional validation
# let's say, when we are going to enforce that even though `q` is optional
# whenever it is provided, it's length doesn't exceed 50 characters.

# Import `Query` and `Annotated`
from fastapi import Query
from typing import Annotated

@app.get('/items-page/')
async def view_items(q: Annotated[str | None, Query(max_length=50)] = None): # additional validation
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# note: Here we are using `Query` because this a query parameter. Later we will see. others like
# `Path()`, `Body()`, `Header()`, and `Cookie()`, that also accept the same arguements as `Query()`

# FastAPI will now:
    # validate the data making sure that the max length is 50 characters
    # show a clear error for the client when the data is not valid
    # Document the parameter in the OpenAPI scheme path operation (so it will show up in the automatic docs UI)

# Query as the default value or in Annotated
'''
@app.get('/query-default-value/')
async def query_default_value(q: Annotated[str, Query(default='joy')] = 'csjoy'): # AssertionError: `Query` default value cannot be set in `Annotated` for 'q'. Set the default value with `=` instead.
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
'''
# ... because it's not clear if the default value shoul;d be "joy" or "csjoy"
# so we would use (preferably): q: Annotated[str, Query()] = 'csjoy'
@app.get('/query-default-value/')
async def query_default_value(q: Annotated[str, Query()] = 'csjoy'):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Advantage of `Annotated`
# Using `Annotated` is recommended instead of the default value in function parameters, it is better for mutltiple reasons.
# we could even use the same function with other tools like: `Typer`

############# 
# Add more validation
##############
@app.get('/add-more-validation/')
async def add_more_validation(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Add regular expression
# regular expression -> A regular expression, regex or regexp is a sequence of characters that define a search pattern for strings
# we can also define a regular expression pattern that hte parameter should match:
@app.get('/add-regular-expression/')
async def add_regula_expression(
    q: Annotated[
        str | None,
        Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:   
        results.update({"q": q})
    return results

'''
The specific regular expression pattern checks that the received parameter value:
# ^ - starts with the following characters, doesn't have characters before.
# fixedquery - has the exact value `fixedquery`
# $ - ends there, doesn't have any more characters after `fixedquery`
'''

# Default values
# let's say, that we want to declare the `q` parameter to haver a `min_length` of `3`, and to have a default value of `fixedquery`:
@app.get('/add-default-values/')
async def add_default_values(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:   
        results.update({"q": q})
    return results
# note: Having a default value of any type, including, `None`, make the parameter optional (not required).

# Required parameters
## when we don't need to declare more validations or metada, we can make the `q` query parameter required
# just by not declaring a default value, like:

# `q: str` instead of `q: str | None = None`
# but when we think to use `Query()`, also make the parameter required, for instance:
@app.get('/required-parameters/')
async def required_params(q: Annotated[str, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:   
        results.update({"q": q})
    return results

# Required, can be `None`
@app.get('/required-can-be-none/')
async def requeired_can_be_none(q: Annotated[str | None, Query(min_length=3)]):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:   
        results.update({"q": q})
    return results

# Query parameter list / multiple values
# when we define a query parameter explicitly with `Query` you can also declare it to receive a list
# list of values, or said in another way, to receive multiple values

# for instance, to declare a query parameter `q` that can appear multiple times in the URL, you can write:
@app.get('/query-parameter-list-or-multiple-values/')
async def query_parameter_list_or_multiple_values(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items

# note: to declare a query parameter with a type of `list`, like in the example, we need to explicitly use `Query`,
# otherwise it would be interpreted as a request body.
# let's test
@app.get('/query-parameter-list-or-multiple-values/test/')
async def query_parameter_list_or_multiple_values_test(q: Annotated[list[str],None]):
    query_items = {"q": q}
    return query_items


# Query parameter list / multiple values with defaults
@app.get('/query-parameter-list-or-multiple-values-with-defaults/')
async def query_parameter_list_or_multiple_values(q: Annotated[list[str] | None, Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

# note:
# # # # keep in mind that in this case, FastAPI won't check the contents of the list
# for instance, `list[int]` would check (and document) that the contents of the list are integers
# but `list` alone wouldn't

# Declare more metadata
# we can add more information about the parameter.
# that information will be included in the generated OpenAPI and used by the documentation user interfaces and external tools
@app.get('/declare-metadata/')
async def declare_metadata(
    q: Annotated[
        str | None, 
        Query(title="Query String",
              description= "Query string for the items to search in the database that have a good match",
              min_length=3
        ),
    ] = None, 
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:   
        results.update({"q": q})
    return results
# note: description is usable**

# Alias parameters
'''
let's imagine that we want the parameter to be `item-query`:
like: `http://localhost:8000/items/?item-query=foobaritems`
but `item-query` is not a valid python variable name
the closest would be `item_query`
but still we need it to be exactly `item-query`...
then we can declare an `alias`, and that alias is what will be used to find the parameter value:
'''
@app.get('/alias-parameters/')
async def alias_parameters(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:   
        results.update({"q": q})
    return results

# Depreciating parameters
# now let's say, we don't like this parameter anymore.
# we have to leave it there a while because there are clients using it, but you want the docs to clearly show it as a depreciated.
# then pass the parameter depreciated=True` to `Query`
@app.get('/depreciate-parameters/')
async def depreciate_parameters(
    q: Annotated[
        str | None,
        Query(
            alias= "item-query",
            title= "Query String",
            description= "description about the parameter",
            min_length=3,
            max_length= 50,
            pattern= "^fixedquery$",
            deprecated= True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Exclude parameters from OpenAPI
# to exclude a query parameter from the generated OpenAPI schema (and thus, from the automatic documentation systems),
# set the parameter `include_in_scheme` of `Query` to `False`:
@app.get('/exclude-parameters-from-openapi/')
async def exclude_parameters_from_openai(hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}



# Custom Validation
'''
There could be cases where we need to do some custom validation that can't be done with the parameters showdn above.
In those cases, we can use a custom validator function that is applied after the normal validation (e.g., after vsalidating the value is a `str`).
we can achieve that using Pydantuc's AfterValidator: `https://docs.pydantic.dev/latest/concepts/validators/#field-after-validator` inside of `Annotated`.
# we can also check BeforeValidator: `https://docs.pydantic.dev/latest/concepts/validators/#field-before-validator`
'''
# For example, this custom validator checks that the item ID starts with `isbn-` for an `ISBN` book number or with `imdb-` for an IMBD movie URL ID
import random
from pydantic import AfterValidator

data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError("Invalid ID format, it must start with 'isbn-' or 'imdb-'")
    return id

@app.get('/custom-validation/')
async def custom_validation(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

# this is works with pydantic v2 or above only


###############################
#### Recap
'''

You can declare additional validations and metadata for your parameters.

## Generic validations and metadata:

- alias
- title
- description
- deprecated

## Validations specific for strings:

- min_length
- max_length
- pattern

## Custom validations using `AfterValidator`.

In these examples you saw how to declare validations for `str` values.

'''