__author__ = 'en0'

from models.redis_document import RedisDocumentFactory
from http import context


BackgroundJobBase = RedisDocumentFactory('jobs', [
    # Name, Req, Pub
    ('status', True, True),
])


class BackgroundJob(BackgroundJobBase):
    @property
    def job_id(self):
        return self.uuid

    @property
    def entity(self):
        _ret = super(BackgroundJob, self).entity
        _ret['job_id'] = self.uuid
        return _ret

    @property
    def private_entity(self):
        _ret = super(BackgroundJob, self).private_entity
        _ret['job_id'] = self.uuid
        return _ret

    def save_and_send(self):
        self.save()
        return self.private_entity, self.status

    @classmethod
    def create(cls, status):
        return super(BackgroundJob, cls).create(dict(status=status))

    @classmethod
    def list(cls):
        _db = context.db
        _jobs = []
        for job_id in _db.hkeys(cls.__document_namespace__):
            _job = super(BackgroundJob, cls).load(job_id)
            _jobs.append(_job.entity)
        return _jobs
