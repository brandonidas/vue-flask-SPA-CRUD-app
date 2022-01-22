import uuid
import sqlite3
from flask import Flask, json, jsonify, request, send_from_directory, abort, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from rng import *

# TODO replace with a real mySQL DB
IMAGES = [
    {
        'id': uuid.uuid4().hex,
        'name' : 'res.png',
        'user' : 'brandonidas',
    },
    {
        'id': uuid.uuid4().hex,
        'name' : 'test.png',
        'user' : 'brandonidas',
    }
]

# acts as a cahce of sorts?
PRODUCTS = [
    {
        'id': uuid.uuid4().hex,
        'name' : 'Pacific Salmon',
        'user' : 'brandonidas',
        'price' : 9,
        'quantity' : 10,
        'tags' : ['fish']
    },
    {
        'id': uuid.uuid4().hex,
        'name' : 'Fish & Chips',
        'user' : 'brandonidas',
        'price' : 132,
        'quantity' : 12,
        'tags' : ['fish','spuds']
    },
    {
        'id': uuid.uuid4().hex,
        'name' : 'Poutine',
        'user' : 'brandonidas',
        'price' : 14,
        'quantity' : 12,
        'tags' : ['spuds']
    }
]

PRODUCTS += generateRandomEntries(20)

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
# TODO figure out relative paths, seems to work BUT MONITOR
app.config["CLIENT_IMAGES"] = "./uploads"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True) # not sure if not HEX.???.
    name=db.Column(db.String(200),nullable=False)
    user=db.Column(db.String(200),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self) :
        return "{} is the name and {} is the price".format(self.name,self.price)

@app.route("/get-image/<image_name>")
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/images', methods=['GET'])
def images():
    print("in images")
    if request.method == 'GET':
        print(IMAGES)
        response_object = {'status': 'success'}
        response_object['images'] = list(reversed(IMAGES))
        return response_object


@app.route('/file-upload', methods=['POST'])
def upload_file():
    print("in file upload")
    response_object = {'status': 'success'}
    if request.method == 'POST':
        if request.files:
            images = request.files.getlist('myFile')
            print(images[0])
            for image in images:
                IMAGES.append(
                    {
                        'name' : image.filename,
                        'id': uuid.uuid4().hex,
                        'user' : 'brandonidas'
                    }
                ) 
                # TODO use system path
                image.save('./uploads/' + image.filename) # must enable permissions

    return jsonify(response_object)


@app.route('/products', methods=['GET', 'POST'])
def all_products():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        PRODUCTS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'user': post_data.get('user'),
            'quantity': post_data.get('quantity'),
            'tags': post_data.get('tags'),
        })
        response_object['message'] = 'Product added!'
    else:
        response_object['products'] = PRODUCTS
    return jsonify(response_object)

@app.route('/products/<product_id>', methods=['PUT', 'DELETE'])
def single_product(product_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_product(product_id)
        print(post_data)
        PRODUCTS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'user': post_data.get('user'),
            'quantity': post_data.get('quantity'),
            'tags': post_data.get('tags'),
        })
        response_object['message'] = 'Product updated!'
    if request.method == 'DELETE':
        remove_product(product_id)
        response_object['message'] = 'Product removed!'
    return jsonify(response_object)

def search_by_term(string):
    # basic search by a single term representing name or user
    pass

# TODO this is where we can expirement with data structures
def search_by_tag(tag):
    pass


def remove_product(product_id):
    for product in PRODUCTS:
        if product['id'] == product_id:
            PRODUCTS.remove(product)
            return True
    return False

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('I just really want an internship!')


if __name__ == '__main__':
    app.run()
