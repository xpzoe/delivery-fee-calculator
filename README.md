# delivery-fee-calculator
This is a simple HTTP API which calculates delivery fee according to some rules. 

Relies on PYTHON and FastAPI. 
# Example #
* ## Request payload(json):
_{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}_

  elements      | type          | unit
  ------------- | --------------|-------
  cart_value    | integer       | cent
  delivery_distance| integer | m
  number_of_items  | integer | none
  time          | string | none
* ## Reseponse payload(json):
_{"delivery_fee": 710}_
  elements      | type          | unit
  ------------- | --------------|-------
  delivery_fee  | integer       | cent
 # Steps #
This API relies on FastAPI Swagger UI. Please redirect to url: http://127.0.0.1:8000/docs (or/your/own/port/docs) to execute the calculator. 

Steps: 
1. Run main.py;
2. Redirect to url: http://127.0.0.1:8000/docs. In Swagger UI, click POST  -> Try it out; 
3. Type the request in the Request body;   
4. Click Execute.
