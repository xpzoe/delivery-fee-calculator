'''
This is an HTTP API which calculates delivery fee.  Created by Pu Xie. 

This API relies on FastAPI Swagger UI. Please redirect to url: http://127.0.0.1:8000/docs to execute the calculator. 
Steps:
    In Swagger UI, click POST  -> Try it out;
    Type the request in the Request body;
    Click Execute.

Example: 
    Request: 
        {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
    Response: 
        {"delivery_fee": 710}
'''


from fastapi import FastAPI
import uvicorn
from pydantic  import BaseModel, Field
from datetime import datetime
import math


class Item(BaseModel):
    '''
    Request Body. Takes care of request validations. 

    cart_value: Value of the shopping cart in cents. Integer, must be larger than 0.
    delivery_distance: Distance between the store and customer's location in meters. Integer, must be larger than 0.
    number_of_items: Number of items in the customer's shopping cart. Integer, must be larger than 0. 
    time: Order time in UTC. In ISO format.
    '''
    cart_value: int = Field(..., gt=0)
    delivery_distance: int = Field(..., gt=0)
    number_of_items: int = Field(..., gt=0)
    time: str = Field(default=..., pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$') # regular expression of ISO format
    
app = FastAPI()

@app.post("/calculator")
async def calculate(item: Item):
    '''
    Calculate the delivery fee based on rules. 
    
    Args:
        item(Item): Information from the request payload.
    
    Returns:
        JSON: {"delivery_fee": int}, calculated delivery fee, will be displayed in the response payload.
    '''

    init_fee = 200 # the lowest delivery fee is 2 euros, without any surcharge
    max_fee = 1500
    surcharge = 0

    # consider cart value
    if item.cart_value < 1000: 
        surcharge += 1000-item.cart_value # calculate surcharge from cart value lower than 10 euros
    elif item.cart_value >= 20000: 
        return {"delivery_fee": 0} # for cart value equal or more than 200 euros
    
    # consider delivery distance
    if item.delivery_distance > 1000:
        surcharge += math.ceil((item.delivery_distance-1000)/500)*100 # calculate surcharge from delivery distance longer than 1000 meters

    # considering numbers of items
    bulk_fee = 120
    if item.number_of_items > 12:
        surcharge += (item.number_of_items-4)*50+bulk_fee # calculate surcharge from number of items above 12
    elif 5 <= item.number_of_items <= 12:
        surcharge += (item.number_of_items-4)*50 # calculate surcharge from number of items above 4 but lower than 13
        
    fee = init_fee+surcharge
    
    # considering Friday rush
    format = '%Y-%m-%dT%H:%M:%SZ'
    date_time = datetime.strptime(item.time, format)
    weekday = date_time.weekday()
    h = date_time.hour
    if weekday == 4 and 15<=h<=19: # check whether it is friday rush
        fee *= 1.2 
    
    return {"delivery_fee": min(fee, max_fee)}


if __name__=='__main__':
    uvicorn.run(app=app,host="127.0.0.1",port=8000)
    