import urllib.request as request
import json
import mysql.connector


def import_data(db):
    insert_data = '''
    INSERT INTO tpe_att(attraction, mrt, type, description, address, traffic, photo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''

    with open("./taipei-attractions.json","r") as res:
        data =  json.load(res)["result"]["results"]

        for i in data:
            
            attraction = i["stitle"]

            mrt = i["MRT"]

            type = i["CAT2"]

            description = i["xbody"]

            address = i["address"]

            traffic = i["info"]

            file = i["file"].split("http")
            photo = ""
            for j in range(len(file)):
                file[j] = file[j].lower()
                if "jpg" in file[j] or "png" in file[j]:
                    photo = f"{photo}http{file[j]}, "

            value = [attraction, mrt, type, description, address, traffic, photo]
            cursor.execute(insert_data, value)
            db.commit()


if __name__ == "__main__":
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "MySQL0126",
        database = "travel",
        auth_plugin = "mysql_native_password"
    )
    cursor = db.cursor()
    import_data(db)
    cursor.close()
