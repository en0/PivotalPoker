__author__ = 'en0'

from models.generic_document import GenericDocumentFactory
import models
from time import sleep


QueueItemBase = GenericDocumentFactory('QueueItem', [
    ('queue_id', True, True),
    ('doc_type', True, True),
    ('data', True, False),
    ('job_id', False, False),
])


class QueueItem(QueueItemBase):
    def __init__(self, queue_id=None, entity=None, document=None, db=None):
        self._job = None
        self._db = db
        if document:
            _json = None
        elif queue_id is None:
            raise KeyError()
        elif entity is None:
            raise KeyError()
        else:
            _json = {
                'queue_id': queue_id,
                'doc_type': entity.__document_namespace__,
                'data': entity.__document__,
            }

        super(QueueItem, self).__init__(json=_json, document=document)

    def set_job_status(self, status, message=None):
        if self._job is None:
            self._job = models.BackgroundJob.load(self.job_id, db=self._db)

        _tries = 10

        if self._job:
            self._job.status = status
            self._job.message = message

            while self._job.save() == 0 and _tries > 1:
                _tries -= 1
                sleep(1)

            return True

        return False
