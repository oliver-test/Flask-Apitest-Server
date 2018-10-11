HTTP_ERRORS = {
    'BadRequest': {
        'status': 400
    },
    'Forbidden': {
        'status': 403
    },
    'NotFound': {
        'status': 404,
        'message': 'The requested URL was not found on the server.'
    },
    'MethodNotAllowed': {
        'status': 405
    },
    'UnprocessableEntity': {
        'status': 422
    }
}


class _SetCode():
    def __init__(self, code=400, msg='bad request'):
        self.code = code
        self.msg = msg


class Code():
    SUCCESS = _SetCode(0, '请求成功')
    BAD_REQUEST = _SetCode(400, 'bad request')
    NOT_FOUND = _SetCode(404, 'not found')

    NO_PARAM = _SetCode(10001, 'no parameter')
    ENV_ALREADY_EXIST = _SetCode(10002, 'env is already exists')

    NAME_ALREADY_EXIST = _SetCode(10003, 'name is already exists')
    API_NOT_FOUNT = _SetCode(10004, 'api not found')

    CLIENT_ERROR = _SetCode(20000, 'client error')

    VALIDATOR_ERROR = _SetCode(30000, 'validator error')

    GENERATOR_ERROR = _SetCode(40000, 'Generator error')

