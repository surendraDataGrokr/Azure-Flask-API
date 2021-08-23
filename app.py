from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma =Marshmallow(app)

# Book Class/Model
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    author = db.Column(db.String(100))

    def __init__(self, book_name, genre, author):
        self.book_name = book_name
        self.genre = genre
        self.author = author

# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('book_id', 'book_name', 'genre' , 'author')

# Init Schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# creation of book data
@app.route('/book', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    genre = request.json['genre']
    author = request.json['author']

    new_book = Book(book_name, genre, author)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

# getting single book details
@app.route('/book/<book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    return book_schema.jsonify(book)

# getting books details
@app.route('/book', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = books_schema.dump(books)
    return books_schema.jsonify(result)

# updating single book details
@app.route('/book/<book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    book.book_name = request.json['book_name']
    book.genre = request.json['genre']
    book.author = request.json['author']
    db.session.commit()
    return book_schema.jsonify(book)
  
# deleting single book details
@app.route('/book/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book)
  

# Run server
if __name__ == '__main__':
    app.run(debug=True)