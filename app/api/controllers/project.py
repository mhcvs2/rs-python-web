from app.api import api
from app.api.services.project import ProjectService


@api.route('/projects', methods=['GET'])
def list_all():
    return ProjectService.get_all_projects()
