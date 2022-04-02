from flask import *
from mysql.connector.pooling import MySQLConnectionPool

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key="jfie3p3rjw"



## MySQL 
db_config = {
    "host" : "localhost",
    "user" : "root",
    "database" : "travel",
    "auth_plugin" : "mysql_native_password",
	"buffered" : True
}


dbpool = MySQLConnectionPool(
                    **db_config,
                    pool_name="my_connection_pool",
                    pool_size=5
                    )


## Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


## api
@app.route("/api/attractions")
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
	headers = {"Accept": "application/json"}

	try:
		if len(query_result) == 12:
				nextpage = page+1 
		else:
			nextpage = None
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
		cursor.close()
		mypool.close()
		return jsonify(nextPage=nextpage, data=res), 200, headers
	except:
		cursor.close()
		mypool.close()
		message = "伺服器內部錯誤"
		return jsonify(error=True, message=message), 500, headers


@app.route("/api/attraction/<attractionID>")
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


@app.route("/api/user",methods=["GET"])
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


@app.route("/api/user",methods=["POST"])
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


@app.route("/api/user",methods=["PATCH"])
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


@app.route("/api/user",methods=["DELETE"])
def logout_api():
	session["status"] = "unlogin"
	session["id"] = ""
	session["user"] = ""
	session["email"] = ""

	response = make_response(jsonify(ok=True), 200)
	response.headers["Accept"] = "application/json"
	return response


@app.route("/api/booking", methods=["GET"])
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
	

@app.route("/api/booking", methods=["POST"])
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


@app.route("/api/booking", methods=["DELETE"])
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


app.run(host="0.0.0.0", port=3000)

