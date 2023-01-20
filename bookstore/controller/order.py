from flask import request
from flask_login import current_user, login_required

from bookstore.application import app
from bookstore.util.result import Result


@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    uid = current_user.id
    ''' TODO 获取购物车的内容，并返回  是一个List[Book]'''
    return Result.success()


@app.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    uid = current_user.id
    bid = request.json.get("bid")
    count = request.json.get("count")
    ''' TODO 在cart表里加上这条记录'''
    return Result.success()


@app.route('/api/cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    uid = current_user.id
    bids = request.json.get("bids") # List[int]
    ''' TODO 在cart表里加上这条记录，无需返回数据'''
    return Result.success()


@app.route('/api/order/create', methods=['POST'])
@login_required
def create_order():
    uid = current_user.id
    bid = request.json.get("bid")  # List[int]
    ''' TODO 用这些书创建订单，返回订单 每本书有多少见shopping_cart表 '''
    return Result.success()