import collections
import itertools
import json
import os
from collections import Counter

import requests

from lib.helpers.test_rail_config_reader import TestRailConfigReader
from lib.test_case import TestCase
from lib.test_in_run import TestInRun
from lib.test_run import TestRun
from path_constants import CACHED_INFO_DIR_PATH, OUTPUT_FILES_DIR_PATH


class ApiRequests:
    __cases = None
    __runs = None
    __failed_tests_file_name = os.path.join(CACHED_INFO_DIR_PATH, "all_failed_tests.txt")

    def __init__(self):
        self.__test_rail_config = TestRailConfigReader()
        self.__headers, self.__auth = {'Content-Type': 'application/json'}, (
            self.__test_rail_config.user, self.__test_rail_config.api_key)

    @property
    def cases(self):
        """Gets information about test cases only the first time during the script execution.
        """
        if self.__cases is None:
            self.__cases = self.__get_cases()

        return self.__cases

    @property
    def runs(self):
        """Gets information about test runs only the first time during the script execution.
        """
        if self.__runs is None:
            self.__runs = self.__get_runs()

        return self.__runs

    def get_not_executed_cases_list(self):
        print("Getting never executed test cases...")
        cases_ids = set([case.id for case in self.cases])
        executed_cases_list, executed_cases_set = self.get_executed_cases_list()

        executed_cases_ids_set = set([case.id for case in executed_cases_set])

        if len(executed_cases_ids_set) > len(cases_ids):
            not_executed_cases_ids_list = list(executed_cases_ids_set - cases_ids)
        else:
            not_executed_cases_ids_list = list(cases_ids - executed_cases_ids_set)

        cases_list = self.__get_cases_list_from_cached_list(not_executed_cases_ids_list)
        output_file_name = os.path.join(OUTPUT_FILES_DIR_PATH, "never_executed_test_cases.txt")

        with open(output_file_name, 'w') as f:
            for test_case in cases_list:
                f.write(f"{test_case.title} {test_case.link}")

        print(f"Finished! Please check {output_file_name} file")

    def get_cases_execution_stats(self):
        executed_cases_list, executed_cases_set = self.get_executed_cases_list()
        return Counter(executed_cases_list)

    def get_executed_cases_list(self):
        executed_case_ids_list = []

        for run in self.runs:
            case_id_in_run_list = [test.case_id for test in self.__get_tests_in_run(run.id)]
            executed_case_ids_list = executed_case_ids_list + case_id_in_run_list

        executed_case_ids_set = set(executed_case_ids_list)
        executed_cases_list, executed_cases_set = self.__get_cases_list_from_cached_list(
            executed_case_ids_list), self.__get_cases_list_from_cached_list(executed_case_ids_set)

        return executed_cases_list, executed_cases_set

    def __get_test_case_info(self, test_ids_list):
        case_info_list = []

        for test_id in test_ids_list:
            test_id_number = int(test_id)
            response = requests.get(f'{self.__test_rail_config.api_address}/get_test/{test_id_number}',
                                    headers=self.__headers,
                                    auth=self.__auth).json()
            case_id = response["case_id"]
            case_title = response["title"]
            case_info_list.append({"test_id": test_id, "case_id": case_id, "case_title": case_title})

        # Write all cases IDs tests for debugging
        failed_case_ids_file_name = os.path.join(CACHED_INFO_DIR_PATH, "failed_case_ids.txt")
        f = open(failed_case_ids_file_name, 'w')
        for failed_case_id in case_info_list:
            f.write(json.dumps(failed_case_id))

        with open(failed_case_ids_file_name) as f:
            chained_failed_tests_list = f.read().splitlines()
            case_info_list = json.loads("[" + chained_failed_tests_list[0].replace("}{", "}, {") + "]")

        return case_info_list

    def get_most_failing_test_cases(self):
        print("Getting the most failing test cases in test runs...")
        chained_failed_tests_list = self.__get_failed_tests_ids()
        case_info_list = self.__get_test_case_info(chained_failed_tests_list)

        # count how many times one unique test case was used
        case_ids_list = [case["case_id"] for case in case_info_list]
        test_case_usages_counter = collections.Counter(case_ids_list)
        most_common_info = test_case_usages_counter.most_common()

        result_file_name = os.path.join(OUTPUT_FILES_DIR_PATH, "the_most_failing_test_cases_in_test_runs.txt")
        with open(result_file_name, 'w') as f:
            for info in most_common_info:
                case_title = list(filter(lambda element: element["case_id"] == info[0], case_info_list))[0][
                    "case_title"]

                f.write(f"{info[0]} {case_title}: {info[1]} times\n")

        print(f"Finished! Please check output_files/{result_file_name} file")

    def get_the_buggiest_test_cases(self):
        failed_tests_ids_list = self.__get_failed_tests_ids()
        tests_with_defects_list = self.__get_failed_tests_defects_list(failed_tests_ids_list)
        case_info_list = self.__get_test_case_info(failed_tests_ids_list)

        test_with_defects_and_case_info_list = []

        # get test_with_defects_and_case_info_list
        for test_with_defect in tests_with_defects_list:
            test_id = test_with_defect["test_id"]
            case_info_for_test_id = [case_info for case_info in case_info_list if case_info["test_id"] == test_id][0]

            test_with_defects_and_case_info_list.append({"defects": test_with_defect["defects"],
                                                         "case_id": case_info_for_test_id["case_id"],
                                                         "case_title": case_info_for_test_id["case_title"]})

        return test_with_defects_and_case_info_list

    def __get_failed_tests_defects_list(self, failed_tests_ids_list):
        tests_with_defects_list = []

        for test_id in failed_tests_ids_list:
            failed_tests_list = requests.get(
                f'{self.__test_rail_config.api_address}/get_results/{test_id}', headers=self.__headers,
                auth=self.__auth).json()

            for failed_test in failed_tests_list:
                tests_with_defects_list.append({"test_id": test_id, "defects": failed_test["defects"]})

        return tests_with_defects_list

    def __get_failed_tests_ids(self):
        test_id_list = []

        # Get IDs of failing tests in test runs
        for run in self.runs:
            failed_status_id = 5
            failed_tests_list = requests.get(
                f'{self.__test_rail_config.api_address}/get_results_for_run/{run.id}&status_id={failed_status_id}',
                headers=self.__headers,
                auth=self.__auth).json()
            test_id_list.append([failed_test["test_id"] for failed_test in failed_tests_list])

        # Chain all lists of failed tests into one array
        chained_failed_tests_list = list(itertools.chain.from_iterable(test_id_list))

        # Write all failed tests for debugging
        with open(self.__failed_tests_file_name, 'w') as f:
            for failed_test in chained_failed_tests_list:
                f.write(f"{failed_test}\n")

        # Use reading of cached chained_failed_tests_list for debugging
        with open(self.__failed_tests_file_name) as f:
            chained_failed_tests_list = f.read().splitlines()

        return chained_failed_tests_list

    def __get_case_from_cached_list(self, case_id):
        case_id = [case for case in self.cases if case.id == case_id]

        if case_id and len(case_id) > 0:
            return case_id[0]
        else:
            return None

    def __get_cases_list_from_cached_list(self, case_ids_list):
        cases_list = [self.__get_case_from_cached_list(case_id) for case_id in case_ids_list]

        return [case for case in cases_list if case and not case.is_deleted]

    def __get_cases(self):
        response = requests.get(
            f'{self.__test_rail_config.api_address}/get_cases/{self.__test_rail_config.project_id}&suite_id={self.__test_rail_config.suite_id}',
            headers=self.__headers,
            auth=self.__auth)

        cases_list = [TestCase(case) for case in response.json()]
        return [case for case in cases_list if not case.is_deleted]

    def __get_tests_in_run(self, run_id):
        response = requests.get(f'{self.__test_rail_config.api_address}/get_tests/{run_id}',
                                headers=self.__headers,
                                auth=self.__auth)

        return [TestInRun(test) for test in response.json()]

    def __get_runs(self):
        response = requests.get(f'{self.__test_rail_config.api_address}/get_runs/{self.__test_rail_config.project_id}',
                                headers=self.__headers,
                                auth=self.__auth)

        return [TestRun(run) for run in response.json()]

    def __get_case(self, case_id):
        response = requests.get(f'{self.__test_rail_config.api_address}/get_case/{case_id}',
                                headers=self.__headers,
                                auth=self.__auth)

        return TestCase(response.json())
