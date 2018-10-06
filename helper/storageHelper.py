import json
import os.path


class StorageHelper:
    __document = None
    __path = None

    @staticmethod
    def write(key, data):
        StorageHelper.__init()
        StorageHelper.__document[key] = json.dumps(data)
        StorageHelper.__store()

    @staticmethod
    def read(key):
        StorageHelper.__init()
        data = StorageHelper.__document[key]
        if data is None:
            return None
        return json.loads(data)

    @staticmethod
    def __init():
        if StorageHelper.__path is None:
            if 'LOCAL_STORAGE' in os.environ:
                StorageHelper.__path = os.environ['LOCAL_STORAGE'] + '/document.json'
            else:
                StorageHelper.__path = '/data/document.json'

        if StorageHelper.__document is None:
            if os.path.isfile(StorageHelper.__path) is False:
                StorageHelper.__document = dict()
            else:
                file = open(StorageHelper.__path)
                StorageHelper.__document = json.load(file)

    @staticmethod
    def __store():
        with open(StorageHelper.__path, 'w+') as file:
            json.dump(StorageHelper.__document, file)
