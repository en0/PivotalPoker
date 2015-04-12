__author__ = 'en0'

from models.generic_document import GenericDocumentFactory


WorkerRequest = GenericDocumentFactory("WorkerRequest", [
    ('request_by', True, True),
    ('action', True, True), # [ 'remove_player' ]
    ('params', True, True)
])
