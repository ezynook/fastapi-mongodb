from fastapi import FastAPI, HTTPException
import pandas as pd
import os, datetime, uvicorn
from pydantic import BaseModel
from pymongo import MongoClient

desc = '''
---

## ```< การใช้งาน FastAPI ร่วมกับ MongoDB />```
### Author: ```Pasit Yodsoi```

---
'''
app = FastAPI(
    title="FastAPI MongoDB Tutorial",
    description=desc,
    version="1.1"
)
db_connection = MongoClient("mongodb://mongodb:27017")
db = db_connection.testdb
collection = db["test"]

now = datetime.datetime.now()
#Data Model
class User(BaseModel):
    _id: str
    firstname: str
    lastname: str
    datetime: str = now
class UpdateVal(BaseModel):
    old_value: str
    firstname_val: str
    lastname_val: str
    
'''----------Query Data------------'''
@app.get("/get/result", tags=["MongoDB"])
async def get_result():
    result = list(collection.find({},{"_id": 0}))
    if result:
        return {
            "status_code": HTTPException(status_code=200, detail="Success"),
            "result": result
        }
    else:
        return {
            "status_code": HTTPException(status_code=404, detail="Error"),
            "result": result
        }

'''----------Query Data Where-------'''
@app.get("/get/result/{firstname}", tags=["MongoDB"])
async def get_result_filter(firstname: str):
    # query = {"firstname": {"$regex": firstname}}, { "_id": 0} //Contains String
    # query = {"firstname": firstname}, { "_id": 0} //Matched String
    result = list(collection.find({"firstname": {"$regex": firstname}}, { "_id": 0}))
    if result:
        return {
            "status_code" : HTTPException(status_code=200, detail="Success"),
            "result" : result
        }
    else:
        return {
            "status_code" : HTTPException(status_code=404, detail="Error"),
            "result" : result
        }

'''-------------Insert Data-------------'''
@app.post("/add/result", tags=["MongoDB"])
async def add_data(user: User):
    data = {
        "firstname": str(user.firstname),
        "lastname": str(user.lastname),
        "datetime": str(now)
    }
    insert = collection.insert_one(data)
    if insert:
        idx = collection.find({"firstname": user.firstname}, {"_id": 1})
        return {
            "status_code": HTTPException(status_code=200, detail="Success"),
            "_id": str(idx[0]["_id"])
        }
    else:
        return HTTPException(status_code=404, detail="Insert Failure")
'''----------------Update Rows----------------'''
@app.post("/get/update/{firstname}/{update}", tags=["MongoDB"])
async def update(value: UpdateVal):
    # myquery = {"firstname": {"$regex": value.old_value}} //รูปแบบ Contains string (Like)
    myquery = { "firstname": value.old_value }
    newvalues = { "$set": { 
        "firstname": value.firstname_val,
        "lastname": value.lastname_val
    } }
    update_val = collection.update_one(myquery, newvalues)
    if update_val:
        return {"status_code": HTTPException(status_code=200, detail="Success")}
    else:
        return {"status_code": HTTPException(status_code=200, detail="Failure")}
'''------------Delete Rows------------'''
@app.delete("/delete/row/{firstname}", tags=["MongoDB"])
async def delete_row(firstname: str):
    # remove_row = {"firstname": {"$regex": firstname}} //รูปแบบ Contains string (Like)
    myquery = { "firstname": firstname }
    remove_row = collection.delete_one(myquery)
    if remove_row:
        return {"status_code": HTTPException(status_code=200, detail="Success")}
    else:
        return {"status_code": HTTPException(status_code=200, detail="Failure")}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)