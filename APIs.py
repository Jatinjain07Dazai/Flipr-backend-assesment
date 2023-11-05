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

count_c, count_o = 0, 0
count_g = 0

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
	Pincode: str = Field(min_length=5, max_length=5) 
	City:str
	Purchase_id:str=Field(None)
	customer_id:str=Field(None)


@app.get("/")
def index():
	return [customer, purchase]


@app.get("/shippment/{city}")
def fetch_ship(city:str):
	output = []
	for i in shipping:
		if shipping[i].City == city:
			output.append(shipping[i])
	return output


@app.get("/Cust_prod/")
def fetch_cust_prod():
	output = []
	for i in customer:
		block=customer[i]
		find = customer[i].customer_id
		for j in purchase:
			prod = []
			if purchase[j].customer_id == find:
				prod.append(purchase[j])
		block["purchaseOrder"] = prod
	output.append(block)
	return output




@app.get("/deep_report/")
def fetch_all():
	output = []
	for i in customer:
		block=customer[i]
		find = customer[i].customer_id
		for j in purchase:
			prod = []
			if purchase[j].customer_id == find:
				temp = purchase[j]
				for k in shipping:
					if temp.purchase_id == shipping[k].Purchase_id:
						temp["ShipmentDetail"] = shipping[k]
						prod.append(temp)
						break
		block["purchaseOrder"] = prod
	output.append(block)
	return output






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
	if ship.customer_id in customer_count and ship.Purchase_id in purchase_count:
		for i in customer:
			if customer[i].customer_id == ship.customer_id:
				global count_g
				count_g += 1
				shipping[count_g] = ship
				return customer[i]
		else:
			return {'Unidentified': 'object'}
