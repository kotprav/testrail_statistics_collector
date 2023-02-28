class TestInRun:
    def __init__(self, req_object: dict[str, int]):
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
    def defects(self) -> list[str]:
        if "defects" in self.__req_object:
            not_parsed_defects = self.__req_object["defects"]

            if not not_parsed_defects:
                return []

            if "," in not_parsed_defects:
                return not_parsed_defects.split(", ")

            return [not_parsed_defects]
        return []

    @property
    def full_info(self) -> dict[str, int]:
        return {"id": self.test_id, "case_id": self.case_id, "status_id": self.status_id, "defects": self.defects}
