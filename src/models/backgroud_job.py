__author__ = 'en0'

from models.redis_document import RedisDocumentFactory
from time import time


BackgroundJobBase = RedisDocumentFactory('jobs', [
    # Name, Req, Pub
    ('status', True, True),
    ('message', False, True),
    ('mtime', False, True),
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

    def save(self):
        # Add modified time but do it directly on the dict
        # as to not flip the dirty flag.
        self.__document__['mtime'] = int(time())
        return super(BackgroundJob, self).save()

    def save_and_send(self):
        self.save()
        return self.private_entity, self.status

    @classmethod
    def create(cls, status, db):
        return super(BackgroundJob, cls).create(dict(status=status), db=db)

    @classmethod
    def list(cls, db):
        _jobs = []
        for job_id in cls.get_document_ids(db):
            _job = super(BackgroundJob, cls).load(job_id, db=db)
            _jobs.append(_job.entity)
        return _jobs
