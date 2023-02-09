class TestInRunResults:
    def __init__(self, test_id, req_object):
        self.__req_object = req_object
        self.__test_id = test_id

    @property
    def test_id(self) -> int:
        return self.__test_id

    @property
    def defects(self) -> list[str]:
        not_parsed_defects = self.__req_object["defects"]

        if not not_parsed_defects:
            return []

        if "," in not_parsed_defects:
            return not_parsed_defects.split(", ")

        return [not_parsed_defects]

    @property
    def full_info(self) -> dict[str, int or list[str]]:
        return {"test_id": self.test_id, "defects": self.defects}
