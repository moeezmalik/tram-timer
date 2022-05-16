from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"name" : "First Data"}

@app.get("/get-time")
def get_tram(stop_id: int):
    return "Hola"