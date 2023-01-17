from lib.helpers.TestRailConfigReader import TestRailConfigReader


class TestCase:
    def __init__(self, resp_object):
        self.__info = resp_object

    @property
    def id(self):
        return self.__info["id"]

    @property
    def is_deleted(self):
        if "is_deleted" in self.__info:
            return self.__info["is_deleted"]
        return None

    @property
    def title(self):
        if "title" in self.__info:
            return self.__info["title"]
        return None

    @property
    def link(self):
        test_rail_config = TestRailConfigReader()

        return f"{test_rail_config.server_address}/index.php?/cases/view/{self.id}"
