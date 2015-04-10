__author__ = 'en0'


from models.generic_document import GenericDocumentFactory
import models


QueueItemBase = GenericDocumentFactory('QueueItem', [
    ('queue_id', True, True),
    ('doc_type', True, True),
    ('data', True, False),
    ('job_id', False, False),
])


class QueueItem(QueueItemBase):
    def __init__(self, queue_id=None, entity=None, document=None):
        self._job = None
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
            self._job = models.BackgroundJob.load(self.job_id)
        if self._job:
            self._job.status = status
            self._job.message = message
            self._job.save()
            return True
        return False
