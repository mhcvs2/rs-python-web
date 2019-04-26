from . import BaseView


class InstanceResourceGroupView(BaseView):

    name = 'group'

    def __init__(self, source):
        super(InstanceResourceGroupView, self).__init__(source)

    def data(self):
        return self.from_data_fields()
