# main.py
import socket


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import pydantic
import subprocess
import uvicorn
import json
import pendulum

from pydantic import BaseModel

app = FastAPI()
characters=[]

@app.get("/")
def root():
    return PlainTextResponse("OK. POST JSON to /pixels, GET /last_roll")

last_roll={}
rolls=[]

@app.post("/pixels")
async def get_dice_info(request: Request):
    # 👇 await works because the function is async
    data = await request.json()
    #print("🎲 Received payload:", json.dumps(data, indent=2))
    face_value=data.get("faceValue")
    print(face_value)
    last_roll.clear()
    last_roll.update(data)
    print(len(rolls))
    if len(rolls)<=1:
        rolls.append(face_value)
    return {"status": "ok", "received": data}



class DnDCharacter(BaseModel):
    name: str
    race: str
    level : int


@app.post("/Insert_new_characters")
def insert_new_characters(character: DnDCharacter):
    new_character = {
        "Character_name": character.name,
        "Race": character.race,
        "Level": character.level
    }
    characters.append(new_character)
    return new_character

@app.get("/characters")
def get_all_characters():
    return characters

@app.get("/rollWithAdvantages")
def roll_with_advantages():
    advantage_roll = 0
    if len(rolls)>1:
        advantage_roll=max(rolls)
    return JSONResponse({"advantage":advantage_roll,"rolls":rolls})


@app.get("/rollWithDisadvantages")
def roll_with_disadvantages():
    disadvantage_roll = 0
    if len(rolls)>1:
        disadvantage_roll = min(rolls)
    return JSONResponse({"Disadvantage":disadvantage_roll,"rolls":rolls})

@app.delete("/ClearRolls")
def clearRolls():
    try:
        rolls.clear()

    except Exception as e:
        print(e)
        return JSONResponse({"status": "error", "message": str(e)})

    return JSONResponse({"status": "ok"})





@app.get("/last_roll")
async def get_last_roll(request: Request):
    if not last_roll:
        return JSONResponse({"message": "No roll has been received yet."}, status_code=404)
    return JSONResponse(last_roll)


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.50.227', port=8000)













