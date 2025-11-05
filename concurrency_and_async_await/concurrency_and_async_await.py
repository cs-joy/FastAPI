### Concurrency and asyn / await
# source: https://fastapi.tiangolo.com/async/#is-concurrency-better-than-parallelism
# self-learning 
# @cs-joy
# resource: FastAPI documentation

# discuss about the `async def` syntax for path operation functions and some backgroundf 
#                                   about asynchronous code, concurrency and parallelism


# TD;DR
        # if we are using third-party libraries that tell us to call them with `await` like:
''' 
response = await third_party_library() 
'''
# then we can declare our path operation functions with `async def` like:
'''
@app.get('/')
async def get_response():
    response = await third_party_library()
    return response
'''
################ NOTE: we can only use `await` inside of functions created with `async def`

# if we are using a third party library that communities with something (a database, an API, the file system and so on) and doesn't
# have suport for using `await`, which is currently the case for most database libraries,
# then we can declare our path operation function as normally, with just `def` syntex:
'''
@app.get('/')
def response():
    res = third_party_lib()
    return res
'''
# it's better to use `async def` instead `def` even when we don't need to use `await` or doesn't have
# to communicate with anything else and wait for it to respond

##########################################

####### Technical Details
    # python supports `asynchronous code` using `coroutines` with `async` and `await`

# asynchronous code
# async and await
# coroutines

### Concurrency and Burgers : https://fastapi.tiangolo.com/async/#concurrent-burgers
# the idea of `asynchronous code` is also sometimes called `concurrency`. it is different from `parallelism`.
# concurrency and parallelism both relate to "different things happening more or less at the same time".

# a fairy tale :) hahahaha
# source: https://fastapi.tiangolo.com/async/#concurrent-burgers

### Parallel Burgers

# comment: asynchronous is better when we consider to work with web application such as API
# souce: learn more : https://fastapi.tiangolo.com/async/#is-concurrency-better-than-parallelism

########## Common examples of CPU bound operations are things that require complex math processing
# for examples:
    # Audio or Image processing
    # Computer vision
    # Machine learning
    # Deep learning 

'''
Concurrency + Parallelism: Web + Machine Learning
sourcel: https://fastapi.tiangolo.com/async/#concurrency-parallelism-web-machine-learning
'''
# perfect solution
# to see how to achieve this parallelism in production see the section about "Deployment :> https://fastapi.tiangolo.com/deployment/"

# # # # # # # # # # # "async and await" # # # # # # # # # # #
# When there is an operation that will require waiting before giving the results and 
# has support for these new Python new features, you can code it like:

# burgers = await get_burgers(2)

# For `await` to work, it has to be inside a function that supports this asynchronicity. To do that
# we just declare it with `async def`: 
'''
async def get_burgers(number: int):
    # Do some asyncrhonous stuff
    return burgers
'''
# instead of `def`:
'''
# this is not asynchronous
def get_sequential_burgers(number: int):
    # Do some sequential stuff
    return burgers
'''
# ith async def, Python knows that, inside that function, it has to be aware of await expressions, and that it can "pause" ⏸ the execution of that function and go do something else 🔀 before coming back.

# When you want to call an async def function, you have to "await" it. So, this won't work:
'''
# this won't work, because get_burgers. was defined with: async def
burgers = get_burgers(2)
'''

# so when we consider to use a library that tells you that you can call it with `await`,
# we need to create the path operation functions that uses it with `async def`:
'''
@app.get('/')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
'''

## More technical details: https://fastapi.tiangolo.com/async/#more-technical-details
# functions defined with `async def` have to be "awaited". So, functions with `async def` 
# can only be called inside of functions defined with `async def` too.

## Write our own async code: https://fastapi.tiangolo.com/async/#write-your-own-async-code
# Starlette(https://starlette.dev)(and FastAPI) are based on AnyIO: https://anyio.readthedocs.io/en/stable/
# Asyncer: https://asyncer.tiangolo.com/,,,, a thin layer on top, to improve a bit the type annotations and get better autocompletion, inline errors, etc.

## Other forms of asynchronous code
# Gevent: https://www.gevent.org/

'''
Coroutines
-----------
this is just the very fancy term for the thing returned by an `async def` function
'''

# FastAPI
    # Starlette
    # AnyIO
        # asyncio
        # Trio

# base_url: https://fastapi.tiangolo.com/async/
#very-technical-details (e.g., source = https://fastapi.tiangolo.com/async/#very-technical-details)
    #path-operation-functions
    #dependencies
    #sub-dependencies
    #other-utility-functions

### let's code
# funniest concept
from fastapi import FastAPI
from fairy_tale_restaurents import Burgers

app = FastAPI()
burger_services = Burgers()

@app.get('/')
def root(): # sequential/synchronous
    print('hey console :)')
    return { "status": "API is running" }

@app.get('/{current_order_no}/{your_orderNo}')
async def need_burgers(current_order_no: int, your_orderNo: int): # asynchronous
    burgers = await burger_services.get_burgers(current_order=current_order_no, your_order_no=your_orderNo)
    return { "is_burger_ready": burgers }


# have a good day #jscript :)
# python3.12