class TestInRun:
    def __init__(self, req_object):
        self.__req_object = req_object

    @property
    def test_id(self):
        return self.__req_object["id"]

    @property
    def case_id(self):
        return self.__req_object["case_id"]
