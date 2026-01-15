from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return { 
        "message": "Hello FastAPI!"
    }

@app.get("/second")
async def read_second():
    return {
        "status": "success"
    }

@app.get("/third")
async def read_third():
    return {
        "domain": "data privacy and security"
    }

@app.get("/fourth")
async def read_fourth():
    return {
        "domain": "f for financial mathematics"
    }

@app.get("/fifth")
async def read_fifth():
    return {
        "message": "unit test with class"
    }