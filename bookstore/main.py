from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from bookstore.application import app
from bookstore.init_db import init_all
import bookstore.controller

if __name__ == '__main__':
    with app.app_context():
        init_all()
        app.run(debug=True)