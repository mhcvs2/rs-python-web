import json
import requests
from oslo_config import cfg
from app.api.views.project import ProjectView
from app.common.decorators import simple_to_view
from app.common.log import get_logger
from app import cache

CONF = cfg.CONF
log = get_logger()


class ProjectServiceError(Exception): pass


class ProjectService(object):
    base_url = CONF.project_service.base_url

    @classmethod
    def _get_headers(cls):
        return {}

    @classmethod
    def _handle_response(cls, response):
        response_str = response.text
        log.info("response: %s", response_str)
        try:
            data = json.loads(response_str)
        except Exception as e:
            raise ProjectServiceError("json deserialize response error: %s" % (str(e)))
        if data['status'] != 200:
            raise ProjectServiceError(data['message'])
        return data['result']

    @classmethod
    def _get(cls, action, data):
        url = "{}{}".format(cls.base_url, action)
        log.info("request get url: %s, data: %s", url, data)
        response = requests.request("GET", url, data=data, headers=cls._get_headers())
        return cls._handle_response(response)

    @classmethod
    @simple_to_view(ProjectView)
    @cache.cached(20, key_prefix="projects")
    def get_all_projects(cls):
        return cls._get("/api/projects", "")
