__author__ = 'en0'

from http import app
from exts.exceptions import ApiException
from http.api.resource_base import ResourceBase, register_route
import models


class Jobs(ResourceBase):
    __uri__ = "/api/v0.1/jobs/"
    __pk__ = "job_id"
    __pk_type__ = "string"
    __method_hints__ = ['GET']

    def get(self, job_id=None):
        if job_id:
            _job = models.BackgroundJob.load(uuid=job_id)
            if _job is None:
                raise ApiException("Not Found", 404)
            _ret = _job.entity
        else:
            _ret = dict(jobs=models.BackgroundJob.list())
        return _ret


register_route(Jobs, app)
