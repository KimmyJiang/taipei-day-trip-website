from email import header, message
from flask import *
import json
from mysql.connector.pooling import MySQLConnectionPool

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


## MySQL 
db_config = {
    "host" : "localhost",
    "user" : "root",
    "password" : "MySQL0126",
    "database" : "travel",
    "auth_plugin" : "mysql_native_password"
}

dbpool = MySQLConnectionPool(
                    **db_config,
                    pool_name="my_connection_pool",
                    pool_size=5
                    )

mypool = dbpool.get_connection()
cursor = mypool.cursor()


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
		return jsonify(nextPage=nextpage, data=res), 200, headers
	except: 
		message = "伺服器內部錯誤"
		return jsonify(error=True, message=message), 500, headers
	
@app.route("/api/attraction/<attractionID>")
def attractionID(attractionID):
	id_query_attraction = '''
		SELECT * FROM tpe_att
		WHERE id = %s
	'''
	id = int(attractionID)

	cursor.execute(id_query_attraction,(id,))
	id_query_result = cursor.fetchall()
	headers = {"Accept": "application/json"}
	
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
			return jsonify(data=data), 200, headers
		else:
			message = "景點編號不正確"
			return jsonify(error = True, message = message), 400, headers
	except:
		message = "伺服器內部錯誤"
		return jsonify(error = True, message = message), 500, headers


app.run(port=3000)
cursor.close()
mypool.close()