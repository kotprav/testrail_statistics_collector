class TestRun:
    def __init__(self, req_object):
        self.__object = req_object

    @property
    def id(self):
        return self.__object["id"]