from lib.helpers.test_rail_config_reader import TestRailConfigReader


class TestCase:
    def __init__(self, resp_object: dict[str, int or str]):
        self.__info = resp_object

    @property
    def id(self) -> int or None:
        return self.__info["id"] if "id" in self.__info else None

    @property
    def is_deleted(self) -> bool or None:
        return self.__info["is_deleted"] if "is_deleted" in self.__info else None

    @property
    def title(self) -> str or None:
        return self.__info["title"] if "title" in self.__info else None

    @property
    def link(self) -> str:
        test_rail_config = TestRailConfigReader()

        return f"{test_rail_config.server_address}/index.php?/cases/view/{self.id}"

    @property
    def full_info(self) -> dict[str, int or str]:
        return {"id": self.id, "title": self.title, "link": self.link}
