

class BaseView(object):

    def __init__(self, source):
        self.source = source

    def data(self):
        pass

    def from_data_fields(self):
        data_fields = getattr(self.source, '_data_fields')
        res = {}
        for data_field in data_fields:
            res[data_field] = getattr(self.source, data_field)
        return res
