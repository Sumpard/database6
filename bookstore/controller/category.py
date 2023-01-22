from bookstore.application import app, db
from bookstore.entity import Category
from bookstore.util.result import Result, modellist2dict


@app.route('/api/category', methods=['GET'])
def get_categories():
    root = db.session.query(Category).filter(Category.parent_id.is_(None)).first()
    result = {
        "tree": root.expand_dto(),
        "all": {c.id: c.to_dto()
                for c in db.session.query(Category).all()},
    }

    return Result.success("", result)
