class TestRun:
    def __init__(self, req_object: dict["id", int]):
        self.__object = req_object

    @property
    def id(self) -> int or None:
        return self.__object["id"] if "id" in self.__object else None

    @property
    def full_info(self) -> dict[str, int]:
        return {"id": self.id}
