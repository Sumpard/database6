from dataclasses import dataclass
from typing import Any, Iterable

from flask import jsonify

from bookstore.application import db


def model2dict(model):
    if isinstance(model, dict):
        return model
    if isinstance(model, Iterable):
        return [model2dict(item) for item in model]
    resultDict = {}
    for k, v in model.__dict__.items():
        if isinstance(v, list):
            v = [model2dict(x) for x in v]
        resultDict[k] = v
    del resultDict['_sa_instance_state']
    return resultDict


def _guarded(data):
    if isinstance(data, (int, float, bool, str)):
        return data
    if isinstance(data, (db.Model, Iterable)):
        return model2dict(data)
    return data


@dataclass
class Result:
    code: int
    message: str
    data: Any

    @staticmethod
    def success(message: str, data: Any = None):
        return jsonify(Result(code=200, message=message, data=_guarded(data)))

    @staticmethod
    def fail(message: str, data: Any = None):
        return jsonify(Result(code=400, message=message, data=_guarded(data)))