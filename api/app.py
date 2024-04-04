from fastapi import FastAPI
import json
from pydantic import BaseModel, Field
import uvicorn
import requests
import mysql.connector

app = FastAPI()

class DataIn(BaseModel):
    text: str = Field(..., title = "Comment to put in database")

class DataOut(BaseModel):
    db_content: list = Field(..., title="list with contet like (id, comment)")
    # id: int = Field(..., title = "ID number of comment in database")
    # comment: str = Field(..., title = "Scraped comment from 4Chan forum")

db_config = {
    "host":"db",
    "port":"3306",
    "user":"my_user",
    "password":"my_password",
    "database":"sentiment_database"
}

@app.get("/data", response_model=DataOut)
async def read_items():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM comments LIMIT 5')
        data = cursor.fetchall()
        # print(data)
        data = {
            "db_content": data
            }
        result_data: DataOut = DataOut(**data)
        return result_data
    except mysql.connector.Error as error:
        return f"Error: {error}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.post("/data_insert")
async def create_items(data: DataIn):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = f'INSERT INTO comments (text_content) VALUES ("{data.text}")'
        cursor.execute(query)
        return {
            "message": "Status OK, data added to db"
            }
    except mysql.connector.Error as error:
        return f"Error: {error}"
    finally:
        if connection.is_connected():
            connection.commit() #need to commit changes, otherwise database wont be updated
            cursor.close()
            connection.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)