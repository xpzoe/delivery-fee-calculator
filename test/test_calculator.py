from fastapi.testclient import TestClient
from main import app

client = TestClient(app=app)

def test_normal():
    '''
    Test on a set of data which leads to normal fee situation.
    
    Return:
            {"delivery_fee": 710}
    '''
    response = client.post('/calculator', 
                           json={
                               "cart_value": 1200,
                               "delivery_distance": 2235,
                               "number_of_items": 4,
                               "time": "2024-01-10T13:00:00Z"
                           }
    )
    assert response.json() == {"delivery_fee": 500}

def test_free_delivery():
    '''
    Test on a set of data which leads to free delivery.
    
    Return:
            {"delivery_fee": 0}
    '''
    response = client.post('/calculator', 
                           json={
                               "cart_value": 120000,
                               "delivery_distance": 2235,
                               "number_of_items": 4,
                               "time": "2024-01-10T13:00:00Z"
                           }
    )
    assert response.json() == {"delivery_fee": 0}

def test_max_fee():
    '''
    Test on a set of data which leads to a max delivery fee.
    
    Return:
            {"delivery_fee": 1500}
    '''
    response = client.post('/calculator', 
                           json={
                               "cart_value": 1200,
                               "delivery_distance": 4000,
                               "number_of_items": 14,
                               "time": "2024-01-12T17:00:00Z"
                           }
    )
    assert response.json() == {"delivery_fee": 1500}
