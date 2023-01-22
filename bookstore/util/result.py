from dataclasses import dataclass
from typing import Any, Iterable

from flask import jsonify

from bookstore.application import db


def model2dict(model, is_simple: bool = False) -> dict:
    resultDict = {}
    if is_simple:
        resultDict = model.__dict__
    else:
        for k, v in model.__dict__.items():
            resultDict[k] = _guarded(v)
    del resultDict['_sa_instance_state']
    return resultDict


def modellist2dict(model_list, is_simple: bool = False) -> list:
    return [_guarded(item, is_simple) for item in model_list]


def _guarded(data, is_simple: bool = False):
    if isinstance(data, db.Model):
        return model2dict(data, is_simple)
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return [_guarded(item, is_simple) for item in data]
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