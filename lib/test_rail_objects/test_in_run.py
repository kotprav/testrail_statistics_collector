class TestInRun:
    def __init__(self, req_object: dict):
        self.__req_object = req_object

    @property
    def id(self) -> int or None:
        return self.__req_object["id"] if "id" in self.__req_object else None

    @property
    def case_id(self) -> int or None:
        return self.__req_object["case_id"] if "case_id" in self.__req_object else None

    @property
    def status_id(self) -> int or None:
        return self.__req_object["status_id"] if "status_id" in self.__req_object else None

    @property
    def defects(self) -> list[str]:
        if "defects" in self.__req_object:
            not_parsed_defects = self.__req_object["defects"]

            if not not_parsed_defects:
                return []

            if "," in not_parsed_defects:
                return not_parsed_defects.split(", ")

            return not_parsed_defects
        return []

    @property
    def full_info(self) -> dict[str, int]:
        return {"id": self.id, "case_id": self.case_id, "status_id": self.status_id, "defects": self.defects}

    def __eq__(self, other):  # pragma: no cover
        if not isinstance(other, TestInRun):
            return NotImplemented

        return self.id == other.id and self.case_id == other.case_id and self.status_id == other.status_id and self.defects == other.defects and self.full_info == other.full_info
