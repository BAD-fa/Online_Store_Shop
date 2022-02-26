from fastapi import FastAPI,status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from setting import db
from models import DiscountCode
from uuid import uuid1

app = FastAPI()

@app.post("/", response_description="make dicountcodes")
def create_discountcode(user_id_list:list,day_expire_time:str):
    result = {}
    for id in user_id_list:
        discount_code = uuid1()
        data_base_object = jsonable_encoder(code)
        code =DiscountCode(user_id=id,expire_time=day_expire_time,code=discount_code)
        try:
            db["codes"].insert_one(data_base_object)
            result[id] = discount_code
        except:
            pass
        return JSONResponse(status_code=status.HTTP_201_CREATED,data={"data":result})
