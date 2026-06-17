from flask import Flask, render_template, request, jsonify
from models.catalog import create_catalog_table, add_catalog_item
import time

app = Flask(__name__)

create_catalog_table()

@app.route("/")
@app.route("/admin_home")
def admin_home_page():
    return render_template("admin/home.html")


@app.route("/admin_catalog")
def admin_catalog_page():
    return render_template("admin/catalog.html")


@app.route("/add_admin_catalog")
def add_admin_catalog_page():
    return render_template("admin/add_catalog.html")


@app.route("/api/add_admin_catalog", methods=["POST"])
def add_admin_catalog_route():
    data = request.get_json()

    name = data.get("name")
    image = data.get("image")
    price = data.get("price")
    description = data.get("description")
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    last_edited_at = "Not edited yet"

    if name and price and image and description:
        add_catalog_item(name, image, price, description, created_at, last_edited_at)
        return jsonify({"success": "Item has been successfully added."})


@app.route("/api/catalog")
def catalog_route():
    return

if __name__ == "__main__":
    app.run(debug=True)