from flask import Flask, jsonify, request
import mysql.connector
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restx import Api, Namespace, Resource, fields

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Inventory Management API",
    "description": "A simple Laptop inventory management API",
    "version": "1.0.0",
}

api = Api(
    app,
    title="Inventory Management API",
    description="A simple laptop management API",
    version="1.0",
    doc= '/swagger/'
)
input_feilds = api.model(
    "Laptop",
    {
        "id": fields.Integer,
        "brand": fields.String,
        "series": fields.String,
        "CPU": fields.String,
        "ram": fields.String,
        "SSD": fields.String,
        "price": fields.Float,
        "Inventory": fields.Integer,
    },
)
input_feilds_update = api.model(
    "Inventory",
    {
        "Inventory": fields.Integer,
    },
)
getlaptop = Namespace("Laptop", path="/api/inventory_management/")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Student1234!",
    database="Inventory_management",
)


@getlaptop.route("/laptop/<int:id>")
class Todos(Resource):
    def get(self, id):
        c = mydb.cursor()
        try:
            c.execute("""SELECT * FROM Laptop WHERE id = %s;""", (id,))
            laptops = c.fetchall()
            if len(laptops) == 0:
                json_data = jsonify({"error": "Id not found"})
                json_data.status_code = 404
                return json_data
            laptop = laptops[0]
            json_data = jsonify(
                {
                    "id": laptop[0],
                    "Brand": laptop[1],
                    "Model": laptop[2],
                    "CPU": laptop[3],
                    "Ram": laptop[4],
                    "Storage": laptop[5],
                    "Price": "$" + str(laptop[6]),
                    "Inventory": str(laptop[7]),
                }
            )
            json_data.status_code = 200
            c.close()
            return json_data
        except ValueError:
            c.close()
            json_data = jsonify({"Error": "Internal server error"})
            json_data.status_code = 500
            return json_data
    @getlaptop.expect(input_feilds_update)
    def put(self, id):
        c = mydb.cursor()
        client = request.json
        rows = count_rows(id)
        if not rows:
            json_data = jsonify({"Error": "Id not found"})
            json_data.status_code = 404
        try:
            if "Inventory" not in client:
                json_data = jsonify({"Error": "Inventory is required"})
                json_data.status_code = 400
                return json_data
            inventory = request.json["Inventory"]
            c.execute(
                """UPDATE Laptop SET Inventory = %s WHERE id = %s;""", (inventory, id)
            )
            mydb.commit()
            c.execute("""SELECT * FROM Laptop WHERE id = %s;""", (id,))
            laptops = c.fetchall()
            laptop = laptops[0]
            json_data = jsonify({
                "Upated Laptop": [
                    {
                    "id": laptop[0],
                    "Brand": laptop[1],
                    "Model": laptop[2],
                    "CPU": laptop[3],
                    "Ram": laptop[4],
                    "Storage": laptop[5],
                    "Price": "$" + str(laptop[6]),
                    "Inventory": str(laptop[7]),
                    }
                ]
            })
            c.close()
            json_data.status_code = 200
            return json_data
        except ValueError:
            c.close()
            json_data = jsonify({"Error": "Internal server error"})
            json_data.status_code = 500
            return json_data

    def delete(self, id):
        c = mydb.cursor()
        rows = count_rows(id)
        if not rows:
            json_data = jsonify({"Error": "Id not found"})
            json_data.status_code = 404
            return json_data
        try:
            c.execute("""DELETE FROM Laptop WHERE id = %s;""", (id,))
            mydb.commit()
            c.close()
            json_data = jsonify({"Succces": "Laptop deleted"})
            json_data.status_code = 200
            return json_data
        except ValueError:
            c.close()
            json_data = jsonify({"Error": "Internal server error"})
            json_data.status_code = 500
            return json_data


@getlaptop.route("/laptop")
class addingLaptop(Resource):
    @getlaptop.expect(input_feilds)
    def post(self):
        c = mydb.cursor()
        client = request.json
        try:
            if "id" not in client:
                json_data = jsonify({"Error": "id is required"})
                json_data.status_code = 400
                return json_data
            if "brand" not in client:
                json_data = jsonify({"Error": "brand is required"})
                json_data.status_code = 400
                return json_data
            if "series" not in client:
                json_data = jsonify({"Error": "series is required"})
                json_data.status_code = 400
                return json_data
            if "CPU" not in client:
                json_data = jsonify({"Error": "CPU is required"})
                json_data.status_code = 400
                return json_data
            if "ram" not in client:
                json_data = jsonify({"Error": "ram is required"})
                json_data.status_code = 400
                return json_data
            if "SSD" not in client:
                json_data = jsonify({"Error": "SSD is required"})
                json_data.status_code = 400
                return json_data
            if "price" not in client:
                json_data = jsonify({"Error": "price is required"})
                json_data.status_code = 400
                return json_data
            if "Inventory" not in client:
                json_data = jsonify({"Error": "Inventory is required"})
                json_data.status_code = 400
                return json_data
            id = request.json["id"]
            rows = count_rows(id)
            if rows:
                json_data = jsonify({"Error": "Id already exist found"})
                json_data.status_code = 409
                return json_data
            brand = request.json["brand"]
            model = request.json["series"]
            cpu = request.json["CPU"]
            ram = request.json["ram"]
            storage = request.json["SSD"]
            price = request.json["price"]
            inventory = request.json["Inventory"]
            print(brand, model, cpu, ram, storage, price, inventory)
            c.execute(
                """INSERT INTO Laptop 
                    (id, brand, series, CPU, ram, SSD, price, Inventory) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                (id, brand, model, cpu, ram, storage, price, inventory),
            )
            mydb.commit()
            c.close()
            json_data = jsonify({"Succces": "Laptop added"})
            json_data.status_code = 201
            return json_data
        except ValueError:
            c.close()
            json_data = jsonify({"Error": "Internal server error"})
            json_data.status_code = 500
            return json_data

def count_rows(id):
    c = mydb.cursor()
    c.execute("SELECT * FROM Laptop WHERE id = %s", (id,))
    rows = c.fetchall()
    if len(rows) == 0:
        return False
    else:
        return True
api.add_namespace(getlaptop)