import collections
import itertools
import os
from typing import Any, Union

from lib.api_requests import ApiRequests
from lib.helpers.cache_config_reader import CacheConfigReader
from lib.helpers.file_helper import write_list_of_dicts_to_file, write_list_to_file
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun
from lib.test_rail_objects.test_in_run_results import TestInRunResults
from lib.test_rail_objects.test_in_run_with_case_info import TestInRunWithCaseInfo
from lib.test_rail_objects.test_run import TestRun
from path_constants import OUTPUT_FILES_DIR_PATH


class ToolApi:
    def __init__(self):
        self.__api_requests = ApiRequests()
        self.__cache_config = CacheConfigReader()

    @property
    def cases(self) -> list[TestCase]:
        return self.__api_requests.cases

    @property
    def runs(self) -> list[TestRun]:
        return self.__api_requests.runs

    def get_not_executed_cases_list(self):
        print("Getting never executed test cases...")
        cases_ids: set[int] = set([case.id for case in self.cases])
        executed_cases_set: list[TestCase] = self.__get_executed_cases_list()
        executed_cases_ids_set: set[int] = set([case.id for case in executed_cases_set])

        if len(executed_cases_ids_set) > len(cases_ids):
            not_executed_cases_ids_list = list(executed_cases_ids_set - cases_ids)
        else:
            not_executed_cases_ids_list = list(cases_ids - executed_cases_ids_set)

        cases_list: list[TestCase] = self.__api_requests.get_test_cases_list_by_id_list(not_executed_cases_ids_list)
        output_file_name: str = os.path.join(OUTPUT_FILES_DIR_PATH, "never_executed_test_cases.txt")

        write_list_of_dicts_to_file(output_file_name,
                                    [f"{test_case.title} {test_case.link}" for test_case in cases_list])

        print(f"Finished! Please check {output_file_name} file")

    def get_most_failing_test_cases(self):
        print("Getting the most failing test cases in test runs...")
        failed_tests_list: list[TestInRun] = self.__api_requests.get_failed_tests()
        failed_tests_with_extended_info: list[TestInRunWithCaseInfo] = []

        for failed_test in failed_tests_list:
            test_case: TestCase = self.__get_test_case_by_test(failed_test)
            if test_case:  # test case might be deleted already
                failed_tests_with_extended_info.append(TestInRunWithCaseInfo(failed_test, test_case))

        # count how many times one unique test case was used
        case_ids_list: list[int] = [failed_test.case_id for failed_test in failed_tests_with_extended_info]
        test_case_usages_counter: collections.Counter = collections.Counter(case_ids_list)
        most_common_info: list[tuple[int, int]] = test_case_usages_counter.most_common()

        result_file_name: str = os.path.join(OUTPUT_FILES_DIR_PATH, "the_most_failing_test_cases_in_test_runs.txt")
        with open(result_file_name, 'w') as f:
            for info in most_common_info:
                case_title: str = \
                    list(filter(lambda element: element.case_id == info[0], failed_tests_with_extended_info))[
                        0].case_title

                f.write(f"{info[0]} {case_title}: {info[1]} times\n")

        print(f"Finished! Please check output_files/{result_file_name} file")

    def get_the_buggiest_tests(self) -> list[
        dict[str, int or list[str]]]:
        failed_tests_list: list[TestInRun] = self.__api_requests.get_failed_tests()
        tests_with_defects_list: list[TestInRunResults] = self.__api_requests.get_failed_tests_defects_list(
            [failed_test.test_id for failed_test in failed_tests_list])

        # merge failed tests with bugs list with information about test cases
        # example result: {'id': 123, 'case_id': 1234, 'status_id': 5, 'test_id': 12345, 'defects': ['JIRA-123']}
        failed_tests_with_bugs_list: list[dict[str, int or list[str]]] = []

        for item1 in failed_tests_list:
            for item2 in tests_with_defects_list:
                if item1.test_id == item2["test_id"]:
                    failed_tests_with_bugs_list.append({**item1.full_info, **item2})

        for item1 in failed_tests_list:
            if not any(d["test_id"] == item1.test_id for d in tests_with_defects_list):
                failed_tests_with_bugs_list.append(item1)

        failed_tests_with_at_least_one_bug_list: list[dict[str, int or list[str]]] = [failed_test for failed_test in
                                                                                      failed_tests_with_bugs_list if
                                                                                      len(failed_test["defects"]) > 0]

        all_defects_list: list[list[str]] = [d['defects'] for d in failed_tests_with_at_least_one_bug_list]
        formatted_all_defects_list: list[str] = list(itertools.chain.from_iterable(all_defects_list))

        defects_count: collections.Counter = collections.Counter(d for d in formatted_all_defects_list)
        most_common_defects: list[tuple[str, int]] = defects_count.most_common()

        test_case_with_bugs_list: list[dict[str, int or list[str]]] = []

        for failed_test in failed_tests_with_at_least_one_bug_list:
            test_case_with_bugs_list.append({"case_id": failed_test["case_id"], "defects": failed_test["defects"]})

        bug_with_test_cases: list[dict[str, str or list]] = []
        for most_common_defect in most_common_defects:
            test_cases_per_bug_list: list[int] = [test_case_with_bug["case_id"] for test_case_with_bug in
                                                  test_case_with_bugs_list
                                                  if
                                                  most_common_defect[0] in test_case_with_bug["defects"]]

            test_cases_titles_per_bug_list: list[dict[str, str or int]] = []
            for case in self.cases:
                for test_case_per_bug in set(test_cases_per_bug_list):
                    if test_case_per_bug == case.id:
                        test_cases_titles_per_bug_list.append({"title": case.title, "case_id": test_case_per_bug})

            bug_with_test_cases.append(
                {"defect": most_common_defect[0], "cases_with_defect": test_cases_titles_per_bug_list})

        output_file_name: str = os.path.join(OUTPUT_FILES_DIR_PATH, "the_worst_bugs.txt")

        write_list_to_file(output_file_name,
                           [f"Defect {test_results['defect']} caused bugs {test_results['cases_with_defect']}\n\n\n" for
                            test_results in
                            bug_with_test_cases])

        return failed_tests_with_bugs_list

    def __get_test_case_by_test(self, test: TestInRun) -> TestCase or None:
        matching_case_list: list[TestCase] = [case for case in self.cases if case.id == test.case_id]

        if matching_case_list:
            return matching_case_list[0]
        return None  # if test case has been deleted already

    def __get_executed_cases_list(self) -> list[TestCase]:
        print("Getting test results from all test runs -> __get_executed_cases_list method")

        executed_cases_set = self.__api_requests.get_test_cases_list_by_id_list(
            set([test_in_run.case_id for test_in_run in self.__api_requests.test_results_from_all_runs]))

        return executed_cases_set
