class TestInRunWithCaseInfo:
    def __init__(self, test, case):
        """

        :param test: TestInRun
        :param case: TestCase
        """
        self.__test = test
        self.__case = case

    @property
    def test_id(self):
        return self.__test.test_id

    @property
    def case_id(self):
        return self.__case.id

    @property
    def case_title(self):
        return self.__case.title

    @property
    def full_info(self):
        return {"test_id": self.test_id, "case_id": self.case_id, "case_title": self.case_title}
