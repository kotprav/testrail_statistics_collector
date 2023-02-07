class TestInRun:
    def __init__(self, req_object: dict["id": int, "case_id": int, "status_id": int]):
        self.__req_object = req_object

    @property
    def test_id(self) -> int:
        return self.__req_object["id"]

    @property
    def case_id(self) -> int:
        return self.__req_object["case_id"]

    @property
    def status_id(self) -> int:
        return self.__req_object["status_id"]

    @property
    def full_info(self) -> dict["id": int, "case_id": int, "status_id": int]:
        return {"id": self.test_id, "case_id": self.case_id, "status_id": self.status_id}
