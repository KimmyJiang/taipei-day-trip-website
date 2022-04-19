from flask import *
from mysql.connector.pooling import MySQLConnectionPool
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
import json


api = Blueprint("api", __name__)
load_dotenv()


## MySQL 
db_config = {
    "host" : os.getenv("mysql_host"),
    "user" : os.getenv("mysql_user"),
	"password" : os.getenv("mysql_password"),
    "database" : os.getenv("database"),
	"buffered" : True
}


dbpool = MySQLConnectionPool(
                    **db_config,
                    pool_name = "my_connection_pool",
                    pool_size = 5
                    )


## api
@api.route("/api/attractions")
def attractions():
	page = int(request.args.get("page", 0))
	keyword = request.args.get("keyword","")

	query_attraction = '''
		SELECT * 
		FROM tpe_att
		WHERE name LIKE %s
		LIMIT %s, %s ;
	'''

	mypool = dbpool.get_connection()
	cursor = mypool.cursor()
	query_data = [f"%{keyword}%", page*12, 12]
	cursor.execute(query_attraction, query_data)
	query_result = cursor.fetchall()
	res = []

	if len(query_result) == 12:
		nextpage = page+1 
	else:
		nextpage = None

	try:
		if len(query_result) > 0:
			for i in range(len(query_result)):
				images = query_result[i][9].split(", ")
				images.remove("")
				data = {
				"id" : query_result[i][0],
				"name" : query_result[i][1],
				"category" : query_result[i][2],
				"description" : query_result[i][3],
				"address" : query_result[i][4],
				"transport" : query_result[i][5],
				"mrt" : query_result[i][6],
				"latitude" : query_result[i][7],
				"longitude" : query_result[i][8],
				"images" : images
				}
				res.append(data)
			result = {
				"nextPage": nextpage,
				"data": res
			}
			code = 200
	except:
		message = "伺服器內部錯誤"
		result = {
			"error": True,
			"message": message
			}
		code = 500
	finally:
		cursor.close()
		mypool.close()
		response = make_response(jsonify(result), code)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/attraction/<attractionID>")
def attractionID(attractionID):
	id_query_attraction = '''
		SELECT * FROM tpe_att
		WHERE id = %s
	'''
	id = int(attractionID)

	mypool = dbpool.get_connection()
	cursor = mypool.cursor()
	cursor.execute(id_query_attraction,(id,))
	id_query_result = cursor.fetchall()

	try:
		if len(id_query_result) == 1:
			images = id_query_result[0][9].split(", ")
			images.remove("")
			data = {
				"id" : id_query_result[0][0],
				"name" : id_query_result[0][1],
				"category" : id_query_result[0][2],
				"description" : id_query_result[0][3],
				"address" : id_query_result[0][4],
				"transport" : id_query_result[0][5],
				"mrt" : id_query_result[0][6],
				"latitude" :id_query_result[0][7],
				"longitude" : id_query_result[0][8],
				"images" : images
			}
			result = {"data":data}
			code = 200
		else:
			result = {"error": True,"message":"景點編號不正確"}
			code = 400
	except:
		result = {"error": True,"message":"伺服器內部錯誤"}
		code = 500
	finally:
		cursor.close()
		mypool.close()
		response = make_response(jsonify(result), code)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/user",methods=["GET"])
def signin_info_api():
	status = session.get("status","unlogin")
	try:
		if status == "login":
			data = {
				"id": session["id"],
				"name": session["user"],
				"email": session["email"]	
			}
		else:
			raise
	except:
		data = None
	finally:
		response = make_response(jsonify(data=data), 200)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/user",methods=["POST"])
def signup_api():
	user_data = request.get_json()
	name = user_data["name"]
	email = user_data["email"]
	password = user_data["password"]
	mypool = dbpool.get_connection()
	cursor = mypool.cursor()
	try:
		if name == "" or email == "" or password == "":
			code = 400
			result = {"error" : True, "message":"註冊失敗，資料不得為空"}
		else: 
			check_user = '''
			SELECT  email
			FROM member
			WHERE email = %s ;
			'''
			cursor.execute(check_user,(email,))
			check_result = cursor.fetchone()
			
			if check_result is None :
				add_user = '''
				INSERT INTO member ( name, email, password )
				VALUES ( %s, %s, %s );
				'''
				cursor.execute(add_user,[name, email, password])
				mypool.commit()
				code = 200
				result = {"ok" : True}
			else:
				code = 400
				result = {"error" : True, "message":"註冊失敗，此 Email 已被註冊"}
	except:
		code = 500
		result = {"error": True, "message":"伺服器內部錯誤"}
	finally:
		cursor.close()
		mypool.close()
		response = make_response(jsonify(result), code)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/user",methods=["PATCH"])
def signin_api():
	login_data = request.get_json()
	email = login_data["email"]
	password = login_data["password"]
	mypool = dbpool.get_connection()
	cursor = mypool.cursor()

	try:
		if email == "" or password =="":
			code = 400
			result = {"error":True, "message":"帳號或密碼不得為空白"}
		else:
			verify_user = '''
				SELECT  id, name, email, password
				FROM member
				WHERE email = %s ;
				'''
			cursor.execute(verify_user,(email,))
			verify_result = cursor.fetchone()
			try:
				pswd = verify_result[3]
				if password == pswd:
					code = 200
					result = {"ok": True}
					session["status"] = "login"
					session["id"] = verify_result[0]
					session["user"] = verify_result[1]
					session["email"] = verify_result[2]
				else:
					raise
			except:
				session["status"] = "unlogin"
				code = 400
				result =  {"error":True, "message":"帳號或密碼錯誤"}
	except:
		code = 500
		result =  {"error":True, "message":"伺服器內部錯誤"}
	finally:
		cursor.close()
		mypool.close()
		response = make_response(jsonify(result), code)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/user",methods=["DELETE"])
def logout_api():
	session["status"] = "unlogin"
	session["id"] = ""
	session["user"] = ""
	session["email"] = ""

	response = make_response(jsonify(ok=True), 200)
	response.headers["Accept"] = "application/json"
	return response


@api.route("/api/booking", methods=["GET"])
def booking_info():
	attractionID = session.get("attractionId", None)
	status = session.get("status","unlogin")
	mypool = dbpool.get_connection()
	cursor = mypool.cursor()

	if status == "login":
		if attractionID :
			attraction_info = '''
			SELECT name, address, images 
			FROM tpe_att
			WHERE id = %s
			'''

			cursor.execute(attraction_info,(attractionID,))
			info = cursor.fetchone()

			code = 200
			result = {
				"data" : {
					"attraction":{
					"id" : attractionID, 
					"name" : info[0], 
					"address" : info[1],
					"image" : info[2].split(", ")[0]
				},
				"date" : session["date"],
				"time" : session["time"],
				"price" : session["price"]
				}
			}
		else:
			code = 200
			result = {"data" : None}
	else:
		code = 403
		result = {"error": True, "message":"請先登入系統"}
	
	cursor.close()
	mypool.close()
	response = make_response(jsonify(result), code)
	response.headers["Accept"] = "application/json"
	return response
	

@api.route("/api/booking", methods=["POST"])
def new_booking():
	booking_info = request.get_json()
	status = session.get("status","unlogin")
	attractionId = booking_info["attractionId"]
	date = booking_info["date"]
	time = booking_info["time"]
	price = booking_info["price"]

	try:
		if status == "login":
			if attractionId == None or date == None or time == None or price == None :
				code = 400
				result = {"error" : True, "message":"資料不得為空"}
			else:
				session["attractionId"] = attractionId
				session["date"] = date
				session["time"] = time
				session["price"] = price
				code = 200
				result = {"ok" : True}
		else:
			code = 403
			result = {"error" : True, "message":"尚未登入系統"}
	except:
		code = 500
		result = {"error": True, "message":"伺服器內部錯誤"}
	finally:
		response = make_response(jsonify(result), code)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/booking", methods=["DELETE"])
def delete_booking():
	status = session.get("status","unlogin")

	if status == "login":
		session["attractionId"] = None
		session["date"] = None
		session["time"] = None
		session["price"] = None
		code = 200
		result = {"ok" : True}
	else:
		code = 403
		result = {"error" : True, "message" : "尚未登入系統"}
	
	response = make_response(jsonify(result), code)
	response.headers["Accept"] = "application/json"
	return response


@api.route("/api/orders", methods=["POST"])
def create_orders():
	status = session.get("status","unlogin")
	order_info = request.get_json()
	contact_name = order_info["order"]["contact"]["name"]
	contact_email = order_info["order"]["contact"]["email"]
	contact_phone = order_info["order"]["contact"]["phone"]
	
	try:
		if status == "login":
			if not contact_name or not contact_email or not contact_phone:
				code = 400
				result = {"error": True, "message":"請輸入完整的聯絡資料"}
			else:
				set_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
				order_number = set_datetime

				add_orders = '''
					INSERT INTO orders (number, price, trip, contact, status )
					VALUES ( %(number)s, %(price)s, %(trip)s, %(contact)s, %(status)s )
				'''

				order_data = {
					"number": order_number,
					"price": order_info["order"]["price"],
					"trip": json.dumps(order_info["order"]["trip"]),
					"contact": json.dumps(order_info["order"]["contact"]),
					"status": 1
				}
					
				mypool = dbpool.get_connection()
				cursor = mypool.cursor()
				cursor.execute(add_orders, order_data)
				mypool.commit()
				cursor.close()
				mypool.close()

				tp_data = {
					"prime": order_info["prime"],
					"partner_key": os.getenv("partner_key"),
					"merchant_id": "kimmy90241_CTBC",
					"amount": order_info["order"]["price"],
					"details": set_datetime,
					"cardholder":{
						"phone_number": contact_phone,
						"name": contact_name,
						"email": contact_email
					}
				}

				url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
				headers = {
					"Content-Type": "application/json",
					"x-api-key": os.getenv("partner_key")
				}

				tp_res = requests.post(url, headers = headers, json=tp_data).json()

				if tp_res["status"] == 0:
					update_order = '''
					UPDATE orders
					SET status = 0
					WHERE number = %s
					'''
					mypool = dbpool.get_connection()
					cursor = mypool.cursor()
					cursor.execute(update_order, (order_number,)) 
					mypool.commit()
					cursor.close()
					mypool.close()

					code = 200
					result = {
						"data": {
							"number": order_number,
							"payment": {
								"status": 0,
								"message": "付款成功"
							}
						}
					}
					
					session["attractionId"] = None
					session["date"] = None
					session["time"] = None
					session["price"] = None
					
				elif tp_res["status"] == 1:
					code = 200
					result = {
						"data": {
							"number": order_number,
							"payment": {
								"status": 1,
								"message": "付款失敗"
							}
						}
					}
				else:
					code = 400
					result = {"error": True, "message":"信用卡資料有誤，請重新輸入"}		
		else:
			code = 403
			result = {"error": True, "message":"請先登入系統"}
	except:
		code = 500
		result = {"error": True, "message":"伺服器內部錯誤"}
	finally:
		response = make_response(jsonify(result), code)
		response.headers["Accept"] = "application/json"
		return response


@api.route("/api/order/<orderNumber>", methods=["GET"])
def order_detail(orderNumber):
	order_number = orderNumber
	status = session.get("status","unlogin")

	if status == "login":
		mypool = dbpool.get_connection()
		cursor = mypool.cursor()

		query_order = '''
		SELECT number, price, trip, contact, status
		FROM orders
		WHERE number = %s 
		'''

		cursor.execute(query_order, (order_number,))
		order_info = cursor.fetchone()
		cursor.close()
		mypool.close()

		if order_info:
			result = {
				"data":{
					"number": order_info[0],
					"price": order_info[1],
					"trip":  json.loads(order_info[2]),
					"contact": json.loads(order_info[3]),
					"status": order_info[4]
				}
			}
			code = 200
		else: 
			code = 200
			result = {"data": None}
	else:
		code = 403
		result = {"error": True, "message":"請先登入系統"}

	response = make_response(jsonify(result), code)
	response.headers["Accept"] = "application/json"
	return response