from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from bookstore.application import app, db
import bookstore.controller


def init():
    from entity.book import Book

    db.drop_all()
    db.create_all()
    Book.init()


if __name__ == '__main__':
    with app.app_context():
        # init()
        app.run(debug=True)