def paging(func, page: int, per_page: int):
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs).paginate(page=page, per_page=per_page, error_out=True)

    return wrapped