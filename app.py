from flask import Flask, render_template, request, jsonify
from models.catalog import create_catalog_table, load_catalog, add_catalog_item
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.sercet_key = os.environ.get("secret_key")

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
    category = data.get("category")
    price = data.get("price")
    description = data.get("description")
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    last_edited_at = "Not edited yet"

    if name and price and image and description and category:
        add_catalog_item(name, image, category, price, description, created_at, last_edited_at)
        return jsonify({"success": "Item has been successfully added."})


@app.route("/edit_admin_catalog")
def edit_admin_page():
    return render_template("admin/edit_catalog.html")


@app.route("/api/catalog")
def catalog_route():
    catalog = load_catalog()
    return jsonify(catalog)

if __name__ == "__main__":
    app.run(debug=True)