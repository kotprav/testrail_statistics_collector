class TestInRunResults:
    def __init__(self, test_id, req_object):
        self.__req_object = req_object
        self.__test_id = test_id

    @property
    def test_id(self):
        return self.__test_id

    @property
    def defects(self):
        return self.__req_object["defects"]

    @property
    def full_info(self):
        return {"test_id": self.test_id, "defects": self.defects }
