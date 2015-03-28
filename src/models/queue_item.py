__author__ = 'en0'


from models.generic_document import GenericDocumentFactory


QueueItem = GenericDocumentFactory('QueueItem', [
    ('queue', True, True),
    ('queue_id', True, True),
    ('data', True, False),
    ('job_id', False, False),
])

