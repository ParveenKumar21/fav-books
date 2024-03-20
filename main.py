from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///all_books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), unique=True, nullable = False)
    author = db.Column(db.String(250), nullable = False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

all_books = []
@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books = all_books)

@app.route('/add', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        new_book = Book(
            title = request.form['title'],
            author = request.form['author'],
            rating = request.form['rating']
        )
        if new_book.title != "" and new_book.author != "" and new_book.rating != "":
            all_books.append(new_book)
            db.session.add(new_book)
            db.session.commit()
            # Now we redirect to the home page to see the added books.
            return redirect(url_for("home"))
    return render_template('add_books.html')

@app.route('/delete')
def delete():
    # get id of the book we want to delete
    book_id = request.args.get("id")
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/edit', methods = ["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        update_book = Book.query.get(book_id)
        update_book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit_rating.html", book = book_selected)

if __name__ == "__main__":
    app.run(debug=True)