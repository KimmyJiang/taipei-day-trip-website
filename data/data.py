import urllib.request as request
import json
import mysql.connector


def import_data(db):
    insert_data = '''
    INSERT INTO tpe_att(name, category, description, address, transport, mrt, latitude, longitude, images)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    with open("./taipei-attractions.json","r") as res:
        data =  json.load(res)["result"]["results"]

        for i in data:
            
            name = i["stitle"]
            category = i["CAT2"]
            description = i["xbody"]
            address = i["address"]
            transport = i["info"]
            mrt = i["MRT"]
            latitude = i["latitude"]
            longitude = i["longitude"]

            file = i["file"].split("http")
            images = ""
            for j in range(len(file)):
                file[j] = file[j].lower()
                if "jpg" in file[j] or "png" in file[j]:
                    images = f"{images}http{file[j]}, "

            value = [name, category, description, address, transport, mrt, latitude, longitude, images]
            cursor.execute(insert_data, value)
            db.commit()


if __name__ == "__main__":
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
	database = "travel",
        auth_plugin = "mysql_native_password"
    )
    cursor = db.cursor()
    import_data(db)
    cursor.close()
