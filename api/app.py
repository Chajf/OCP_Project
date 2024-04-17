from fastapi import FastAPI, HTTPException
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

class CountOut(BaseModel):
    db_count: int = Field(..., title="Rows count in database")
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

@app.get("/data_count", response_model=CountOut)
async def count_items():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM comments"
        cursor.execute(query)
        row_count = cursor.fetchone()[0]

        data = {
            "db_count": row_count
            }
        result_data: CountOut = CountOut(**data)
        return result_data
    except mysql.connector.Error as error:
        return f"Error: {error}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.post("/db_clear")
async def clear_table():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = 'DELETE FROM comments'
        cursor.execute(query)
        return {
            "message": "Status OK, db table 'comments' cleard"
            }
    except mysql.connector.Error as error:
        return f"Error: {error}"
    finally:
        if connection.is_connected():
            connection.commit() #need to commit changes, otherwise database wont be updated
            cursor.close()
            connection.close()

@app.post("/link")
async def get_link(link: dict):
    try:
        page_link = link.get("link")
        if page_link:
            scrape_response = requests.get(f"http://scrape:7000/scrape?link={page_link}")
            if scrape_response.status_code == 200:
                scrape_data = scrape_response.json()
                insert_response = data_insert(scrape_data)
                if insert_response.get("message")=="Status OK, data added to db":
                    return {"message": "Page scraped and data inserted into database successfully"}
                else:
                    raise HTTPException(status_code=insert_response.status_code, detail="Failed to insert data into database")
                # if insert_response.status_code == 200:
                #     return {"message": "Page scraped and data inserted into database successfully"}
                # else:
                #     raise HTTPException(status_code=insert_response.status_code, detail="Failed to insert data into database")
            else:
                raise HTTPException(status_code=scrape_response.status_code, detail="Scraping failed")
        else:
            raise HTTPException(status_code=400, detail="Link not provided.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.post("/status")
async def check_model():
    model_status = requests.get("http://model:6000/check_model")
    print(model_status.json())
    return {"message":"Connection OK"}

@app.post("/prediction")
async def predict_sentiment():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = f'SELECT text_content FROM comments LIMIT 5'
        cursor.execute(query)
        comments = cursor.fetchall()
        comments = [comment[0] for comment in comments]
        preds = requests.post("http://model:6000/predict", json={"data":comments})
        return {"result": preds.json()}
    except mysql.connector.Error as error:
        return f"Error: {error}"
    finally:
        if connection.is_connected():
            connection.commit() #need to commit changes, otherwise database wont be updated
            cursor.close()
            connection.close()
    
def data_insert(data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        comments = data.get("text_contents")
        for item in comments:
            query = f'INSERT INTO comments (text_content) VALUES ("{item}")'
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