from flask import Flask, render_template, request, jsonify
from models.catalog import create_catalog_table, load_catalog, add_catalog_item
import time
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

app = Flask(__name__)

load_dotenv()
app.secret_key = os.environ.get("secret_key")

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

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
    name = request.form.get("name")
    category = request.form.get("category")
    price = request.form.get("price")
    description = request.form.get("description")
    created_at = time.strftime("%Y-%m-%d %H:%M:%S")
    last_edited_at = "Not edited yet"

    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)

    if name and price and description and category:
        add_catalog_item(name, image_path, category, price, description, created_at, last_edited_at)
        return jsonify({"success": "Item has been successfully added."})

    return jsonify({'error': 'Missing required fields'}), 400


@app.route("/edit_admin_catalog")
def edit_admin_page():
    return render_template("admin/edit_catalog.html")


@app.route("/api/catalog")
def catalog_route():
    catalog = load_catalog()
    return jsonify(catalog)

if __name__ == "__main__":
    app.run(debug=True)