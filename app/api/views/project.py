from . import BaseView


class ProjectView(BaseView):

    def __init__(self, source):
        super(ProjectView, self).__init__(source)

    def data(self):
        return self.source
