from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID, uuid4, uuid1
from random import randint
from collections import defaultdict

app = FastAPI()

customer = defaultdict()

purchase = defaultdict()

shipping = defaultdict()


customer_count =set()
purchase_count = set()


def id_genrator():
	return "".join([str(randint(0,99)) for i in range(15)])


class Customer(BaseModel):
	customer_name: str
	Email: str
	Mobile_Number: str = Field(min_length=5) 
	City:str
	customer_id:str=Field(default_factory=id_genrator)


class Purchase(BaseModel):
	product_name: str
	Qunatity: int
	MRP: int 
	Pricing: int 
	purchase_id:str=Field(default_factory=id_genrator)
	customer_id:str=Field(None)


class Shipping(BaseModel):
	Address: str
	City: str
	Pincode: int = Field(min_length=5, max_length=5) 
	City:str
	Purchase_id:str=Field(None)
	customer_id:str=Field(None)


@app.get("/")
def index():
	return customer


count_c, count_o = 0, 0
count_g = 0

@app.post("/create_customer")
def create_customer(custom:Customer):
	global count_c
	count_c += 1
	customer[count_c] = custom
	customer_count.add(custom.customer_id)
	return {'Passed': 'True'}



@app.post("/place_order")
def place_order(order:Purchase):
	if order.customer_id in customer_count: 
		global count_o
		count_o += 1
		purchase[count_o] = order
		purchase_count.add(order.purchase_id)
		return {'Passed': 'True'}
	else:
		return {"unregisted": "id" }



@app.post("/ship_product")
def ship_product(ship:Shipping):
	if ship.Purchase_id in purchase_count and ship.customer_id in customer_count:
		global count_g
		count_g += 1
		shipping[count_g] = ship
		return {'Passed': 'True'}
	else:
		return {'Unidentified': 'object'}
