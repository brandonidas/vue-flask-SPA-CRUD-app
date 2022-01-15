import uuid
from flask import Flask, json, jsonify, request, send_from_directory, abort
from flask_cors import CORS

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

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

'''
curl -X POST http://127.0.0.1:5000/books -d \
  '{"title": "1Q84", "author": "Haruki Murakami", "read": "true"}' \
  -H 'Content-Type: application/json'
'''

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
# TODO figure out relative paths
app.config["CLIENT_IMAGES"] = "/Users/brandontong/Documents/github/vue-flask-SPA-CRUD-app/server/uploads"

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

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
        response_object = {'status': 'success'}
        response_object['images'] = IMAGES
        return response_object


@app.route('/file-upload', methods=['POST'])
def upload_file():
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
                image.save('/Users/brandontong/Documents/github/vue-flask-SPA-CRUD-app/server/uploads/' + image.filename) # must enable permissions

    return jsonify(response_object)


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('I just really want an internship!')


if __name__ == '__main__':
    app.run()
