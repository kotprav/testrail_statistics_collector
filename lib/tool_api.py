import collections
import os

from lib.api_requests import ApiRequests
from lib.helpers.cache_config_reader import CacheConfigReader
from lib.helpers.file_helper import write_list_of_dicts_to_file
from lib.test_rail_objects.test_in_run_with_extended_info import TestInRunWithExtendedInfo
from path_constants import OUTPUT_FILES_DIR_PATH


class ToolApi:
    def __init__(self):
        self.__api_requests = ApiRequests()
        self.__cache_config = CacheConfigReader()

    @property
    def cases(self):
        return self.__api_requests.cases

    @property
    def runs(self):
        return self.__api_requests.runs

    def get_not_executed_cases_list(self):
        print("Getting never executed test cases...")
        cases_ids = set([case.id for case in self.cases])
        executed_cases_set = self.__get_executed_cases_list()
        executed_cases_ids_set = set([case.id for case in executed_cases_set])

        if len(executed_cases_ids_set) > len(cases_ids):
            not_executed_cases_ids_list = list(executed_cases_ids_set - cases_ids)
        else:
            not_executed_cases_ids_list = list(cases_ids - executed_cases_ids_set)

        cases_list = self.__api_requests.get_test_cases_list_by_id_list(not_executed_cases_ids_list)
        output_file_name = os.path.join(OUTPUT_FILES_DIR_PATH, "never_executed_test_cases.txt")

        write_list_of_dicts_to_file(output_file_name,
                                    [f"{test_case.title} {test_case.link}" for test_case in cases_list])

        print(f"Finished! Please check {output_file_name} file")

    def get_most_failing_test_cases(self):
        print("Getting the most failing test cases in test runs...")
        failed_tests_list = self.__api_requests.get_failed_tests()
        failed_tests_with_extended_info = []

        for failed_test in failed_tests_list:
            test_case = self.__get_test_case_by_test(failed_test)
            if test_case:  # test case might be deleted already
                failed_tests_with_extended_info.append(TestInRunWithExtendedInfo(failed_test, test_case))

        # count how many times one unique test case was used
        case_ids_list = [failed_test.case_id for failed_test in failed_tests_with_extended_info]
        test_case_usages_counter = collections.Counter(case_ids_list)
        most_common_info = test_case_usages_counter.most_common()

        result_file_name = os.path.join(OUTPUT_FILES_DIR_PATH, "the_most_failing_test_cases_in_test_runs.txt")
        with open(result_file_name, 'w') as f:
            for info in most_common_info:
                case_title = \
                    list(filter(lambda element: element.case_id == info[0], failed_tests_with_extended_info))[
                        0].case_title

                f.write(f"{info[0]} {case_title}: {info[1]} times\n")

        print(f"Finished! Please check output_files/{result_file_name} file")

    def get_the_buggiest_test_cases(self):
        failed_tests_list = self.__api_requests.get_failed_tests()
        tests_with_defects_list = self.__api_requests.get_failed_tests_defects_list(
            [failed_test.test_id for failed_test in failed_tests_list])
        case_info_list = self.__api_requests.get_test_with_result(failed_tests_list)

        test_with_defects_and_case_info_list = []

        # get test_with_defects_and_case_info_list
        for test_with_defect in tests_with_defects_list:
            test_id = test_with_defect["test_id"]
            case_info_for_test_id = [case_info for case_info in case_info_list if case_info["test_id"] == test_id][0]

            test_with_defects_and_case_info_list.append({"defects": test_with_defect["defects"],
                                                         "case_id": case_info_for_test_id["case_id"],
                                                         "case_title": case_info_for_test_id["case_title"]})

        return test_with_defects_and_case_info_list

    def __get_test_case_by_test(self, test):
        """

        :param test: TestInRun
        :return: TestCase
        """
        matching_case_list = [case for case in self.cases if case.id == test.case_id]

        if matching_case_list:
            return matching_case_list[0]
        return None  # if test case has been deleted already

    def __get_executed_cases_list(self):
        """

        :return: TestCase[]
        """
        tests_in_run_list = self.__api_requests.get_test_results_from_all_test_runs()

        executed_cases_set = self.__api_requests.get_test_cases_list_by_id_list(
            set([test_in_run.case_id for test_in_run in tests_in_run_list]))

        return executed_cases_set
