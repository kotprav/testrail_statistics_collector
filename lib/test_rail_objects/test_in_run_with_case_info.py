from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun


class TestInRunWithCaseInfo:
    def __init__(self, test: TestInRun, case: TestCase):  # pragma: no cover
        self.__test = test
        self.__case = case

    @property
    def test_id(self) -> int:
        return self.__test.id

    @property
    def case_id(self) -> int:
        return self.__case.id

    @property
    def case_title(self) -> str:
        return self.__case.title

    @property
    def full_info(self) -> dict[str, int or str]:
        return {"test_id": self.test_id, "case_id": self.case_id, "case_title": self.case_title}
