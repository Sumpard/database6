from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from bookstore.application import app
import bookstore.controller

if __name__ == '__main__':
    with app.app_context():
        app.run(port=5000, debug=True)