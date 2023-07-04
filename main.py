from fastapi import FastAPI
from GetFromBWEGT import getETAOfNextMOT, Status
import json

app = FastAPI()

print("hello")

@app.get("/")
def index():
    return {"Hello" : "World"}

@app.get("/get-time")
def get_tram(stop_id, target_line, target_direction):
    reply = getETAOfNextMOT(stop_id, target_line, target_direction)
    reply['status'] = reply['status'].value
    json_object = json.dumps(reply)
    return json_object