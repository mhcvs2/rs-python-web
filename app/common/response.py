

class ResponseCode(object):

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


class ResponseCodeEnum(object):
    SUCCESS = ResponseCode(200, 'success')
    NOT_LOGIN = ResponseCode(401, 'not login')
    ERROR = ResponseCode(500, 'error')


class Response(dict):

    def __init__(self, code=ResponseCodeEnum.SUCCESS, msg=None, result=None):
        super(Response, self).__init__()
        self['status'] = code.code
        self['message'] = msg if msg is not None else code.msg
        self['result'] = result if result is not None else []
