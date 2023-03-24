import collections
import itertools
import os

from lib.api_requests import ApiRequests
from lib.helpers.file_helper import write_list_of_dicts_to_file, write_list_to_file
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun
from lib.test_rail_objects.test_in_run_with_case_info import TestInRunWithCaseInfo
from path_constants import OUTPUT_FILES_DIR_PATH


class ToolApi:
    def __init__(self):
        self.__api_requests = ApiRequests()

    def save_not_executed_cases_list(self):
        print("Getting never executed test cases...")
        cases_ids: set[int] = {case.id for case in self.__api_requests.cases}
        executed_cases_ids_set: set[int] = self.__get_executed_cases_ids_list()
        not_executed_cases_ids_list: list[int] = self.__get_not_executed_cases_ids(cases_ids, executed_cases_ids_set)

        not_executed_cases_list: list[TestCase] = self.__get_test_cases_list_by_id_list(
            not_executed_cases_ids_list)

        self.__write_info_about_not_executed_cases_list(not_executed_cases_list)

    def save_most_failing_test_cases(self):
        print("Getting the most failing test cases in test runs...")

        failed_tests_with_extended_info_list: list[TestInRunWithCaseInfo] = self.__get_failed_tests_with_extended_info(
            self.__api_requests.failed_tests)

        test_cases_usage_info: list[tuple[int, int]] = self.__get_test_case_usage_info(
            failed_tests_with_extended_info_list)

        self.__write_info_about_most_failing_test_cases(test_cases_usage_info, failed_tests_with_extended_info_list)

    def save_the_buggiest_tests(self):
        print("Getting the buggiest tests...")
        tests_with_defects_list: list[TestInRun] = self.__get_tests_with_defects_list()

        # merge failed tests with bugs list with information about test cases
        # example result: {'id': 123, 'case_id': 1234, 'status_id': 5, 'test_id': 12345, 'defects': ['JIRA-123']}
        failed_tests_with_bugs_list: list[TestInRun] = self.__get_failed_tests_with_bugs_list(
            tests_with_defects_list)

        self.__save_info_about_the_buggiest_tests(failed_tests_with_bugs_list)

    def __save_info_about_the_buggiest_tests(self, failed_tests_with_bugs_list: list[TestInRun]):
        failed_tests_with_at_least_one_bug_list: list[TestInRun] = self.__get_failed_tests_with_at_least_one_bug_list(
            failed_tests_with_bugs_list)

        formatted_all_defects_list: list[str] = self.__get_all_defects_list(failed_tests_with_at_least_one_bug_list)
        most_common_defects: list[tuple[str, int]] = self.__get_most_common_defects(formatted_all_defects_list)

        test_case_with_bugs_list: list[dict[str, int or list[str]]] = self.__get_test_case_with_bugs_list(
            failed_tests_with_at_least_one_bug_list)

        bug_with_test_cases: list[dict[str, str or list]] = self.__get_bug_with_test_cases(most_common_defects,
                                                                                           test_case_with_bugs_list)

        self.__write_info_about_the_buggiest_tests(bug_with_test_cases)

    def __write_info_about_not_executed_cases_list(self, not_executed_cases_list: list[TestCase]):
        output_file_name: str = os.path.join(OUTPUT_FILES_DIR_PATH, "never_executed_test_cases.txt")

        write_list_of_dicts_to_file(output_file_name,
                                    [f"{test_case.title} {test_case.link}" for test_case in not_executed_cases_list])

        self.__write_result_logs(output_file_name)

    def __write_info_about_most_failing_test_cases(self, test_cases_usage_info: list[tuple[int, int]],
                                                   failed_tests_with_extended_info_list: list[TestInRunWithCaseInfo]):
        result_file_name: str = os.path.join(OUTPUT_FILES_DIR_PATH, "the_most_failing_test_cases_in_test_runs.txt")

        with open(result_file_name, 'w') as file:
            for info in test_cases_usage_info:
                case_title: str = \
                    list(filter(lambda element: element.case_id == info[0], failed_tests_with_extended_info_list))[
                        0].case_title

                file.write(f"{info[0]} {case_title}: {info[1]} times\n")

        self.__write_result_logs(result_file_name)

    def __write_info_about_the_buggiest_tests(self, bug_with_test_cases: list[dict[str, str or list]]):
        output_file_name: str = os.path.join(OUTPUT_FILES_DIR_PATH, "the_worst_bugs.txt")

        write_list_to_file(output_file_name,
                           [f"Defect {test_results['defect']} caused bugs {test_results['cases_with_defect']}\n\n\n" for
                            test_results in
                            bug_with_test_cases])

        self.__write_result_logs(output_file_name)

    def __get_test_case_by_test(self, test: TestInRun) -> TestCase or None:
        matching_case_list: list[TestCase] = [case for case in self.__api_requests.cases if case.id == test.case_id]

        if matching_case_list:
            return matching_case_list[0]
        return None  # if test case has been deleted already

    def __get_executed_cases_ids_list(self) -> set[int]:
        executed_cases_set = self.__get_test_cases_list_by_id_list(
            {test_in_run.case_id for test_in_run in self.__api_requests.get_test_results_from_all_runs()})

        executed_cases_ids_set: set[int] = {case.id for case in executed_cases_set}

        return executed_cases_ids_set

    @staticmethod
    def __get_test_case_usage_info(failed_tests_list: list[TestInRunWithCaseInfo]) -> list[tuple[int, int]]:
        case_ids_list: list[int] = [failed_test.case_id for failed_test in failed_tests_list]
        test_case_usages_counter: collections.Counter = collections.Counter(case_ids_list)
        most_common_info: list[tuple[int, int]] = test_case_usages_counter.most_common()

        return most_common_info

    def __get_failed_tests_with_extended_info(self, failed_tests_list: list[TestInRun]) -> list[TestInRunWithCaseInfo]:
        failed_tests_with_extended_info: list[TestInRunWithCaseInfo] = []

        for failed_test in failed_tests_list:
            test_case: TestCase = self.__get_test_case_by_test(failed_test)
            if test_case:  # test case might be deleted already
                failed_tests_with_extended_info.append(TestInRunWithCaseInfo(failed_test, test_case))

        return failed_tests_with_extended_info

    @staticmethod
    def __get_not_executed_cases_ids(cases_ids: set[int], executed_cases_ids_set: set[int]) -> list[int]:
        if len(executed_cases_ids_set) > len(cases_ids):
            not_executed_cases_ids_list = list(executed_cases_ids_set - cases_ids)
        else:
            not_executed_cases_ids_list = list(cases_ids - executed_cases_ids_set)

        return not_executed_cases_ids_list

    def __get_test_cases_list_by_id_list(self, id_list: list[int] or set[int]) -> list[TestCase]:
        return [case for case in self.__api_requests.cases if case.id in id_list]

    def __get_tests_with_defects_list(self) -> list[TestInRun]:
        return self.__api_requests.get_failed_tests_defects_list(
            [failed_test.id for failed_test in self.__api_requests.failed_tests])

    def __get_failed_tests_with_bugs_list(self, tests_with_defects_list: list[TestInRun]) -> list[TestInRun]:
        # merge failed tests with bugs list with information about test cases
        # example result: {'id': 123, 'case_id': 1234, 'status_id': 5, 'test_id': 12345, 'defects': ['JIRA-123']}
        if len(tests_with_defects_list) <= len(self.__api_requests.failed_tests):
            return self.__get_intersected_failed_tests_with_bugs_list(
                self.__api_requests.failed_tests, tests_with_defects_list)
        else:
            return self.__get_intersected_failed_tests_with_bugs_list(tests_with_defects_list,
                                                                      self.__api_requests.failed_tests)

    @staticmethod
    def __get_intersected_failed_tests_with_bugs_list(bigger_list: list[TestInRun], smaller_list: list[TestInRun]):
        failed_tests_with_bugs_list: list[list[TestInRun]] = []

        for smaller_list_item in smaller_list:
            intersected_elements_list = [
                TestInRun({"case_id": smaller_list_item.case_id, "id": smaller_list_item.id,
                           "status_id": smaller_list_item.status_id,
                           "defects": bigger_list_item.defects})
                for
                bigger_list_item in
                bigger_list if
                smaller_list_item.id == bigger_list_item.id]

            if intersected_elements_list:
                failed_tests_with_bugs_list.append(intersected_elements_list)

        return [item for sublist in failed_tests_with_bugs_list for item in sublist]

    @staticmethod
    def __get_failed_tests_with_at_least_one_bug_list(failed_tests_with_bugs_list: list[TestInRun]) -> \
            list[TestInRun]:
        return [failed_test for failed_test in failed_tests_with_bugs_list if len(failed_test.defects) > 0]

    @staticmethod
    def __get_all_defects_list(failed_tests_with_at_least_one_bug_list: list[TestInRun]) -> list[str]:
        all_defects_list: list[list[str]] = [failed_test.defects for failed_test in
                                             failed_tests_with_at_least_one_bug_list]

        return list(itertools.chain.from_iterable(all_defects_list))

    @staticmethod
    def __get_most_common_defects(all_defects_list: list[str]) -> list[tuple[str, int]]:
        defects_count: collections.Counter = collections.Counter(d for d in all_defects_list)
        return defects_count.most_common()

    @staticmethod
    def __get_test_case_with_bugs_list(failed_tests_with_at_least_one_bug_list: list[TestInRun]) -> \
            list[dict[str, int or list[str]]]:
        return [{"case_id": failed_test.case_id, "defects": failed_test.defects} for failed_test in
                failed_tests_with_at_least_one_bug_list]

    def __get_bug_with_test_cases(self, most_common_defects: list[tuple[str, int]],
                                  test_case_with_bugs_list: list[dict[str, int or list[str]]]) -> list[
        dict[str, str or list]]:
        bug_with_test_cases: list[dict[str, str or list]] = []

        for most_common_defect in most_common_defects:
            test_cases_per_bug_list: list[int] = [test_case_with_bug["case_id"] for test_case_with_bug in
                                                  test_case_with_bugs_list
                                                  if
                                                  most_common_defect[0] in test_case_with_bug["defects"]]

            test_cases_titles_per_bug_list: list[dict[str, str or int]] = []
            for case in self.__api_requests.cases:
                for test_case_per_bug in set(test_cases_per_bug_list):
                    if test_case_per_bug == case.id:
                        test_cases_titles_per_bug_list.append({"title": case.title, "case_id": test_case_per_bug})

            bug_with_test_cases.append(
                {"defect": most_common_defect[0], "cases_with_defect": test_cases_titles_per_bug_list})

        return bug_with_test_cases

    @staticmethod
    def __write_result_logs(file_name: str):
        print(f"૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა Finished! Please check output_files/{file_name} file")
