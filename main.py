from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine,text
import uvicorn
app = FastAPI()

class TestData(BaseModel):
    dbtype:str
    ip: str
    port: str
    id:str
    pw:str
    dbname: str
    sql : str

        
@app.post("/test/")
async def test(data: TestData):
    result = None
    if data.dbtype in ["mariadb","mysql"]:
        engine = create_engine(f"mysql+pymysql://{data.id}:{data.pw}@{data.ip}:{data.port}/{data.dbname}")
    elif data.dbtype == "postgresql":
        engine = create_engine(f"postgresql+psycopg2://{data.id}:{data.pw}@{data.ip}:{data.port}/{data.dbname}")
    with engine.connect() as connection:
        result = connection.execute(text(data.sql))
    return str(list(result))

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", access_log=True, port=8080)