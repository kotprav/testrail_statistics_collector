class TestRun:
    def __init__(self, req_object: dict["id", int]):
        self.__object = req_object

    @property
    def id(self) -> int:
        return self.__object["id"]

    @property
    def full_info(self) -> dict["id", int]:
        return {"id": self.id}
