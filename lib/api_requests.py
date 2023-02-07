import itertools
import os

import requests

from lib.helpers.cache_config_reader import CacheConfigReader
from lib.helpers.file_helper import read_list_of_dicts_from_file, write_list_of_dicts_to_file
from lib.helpers.test_rail_config_reader import TestRailConfigReader
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun
from lib.test_rail_objects.test_in_run_results import TestInRunResults
from lib.test_rail_objects.test_run import TestRun
from path_constants import CACHED_INFO_DIR_PATH


class ApiRequests:
    def __init__(self):
        self.__test_rail_config = TestRailConfigReader()
        self.__cache_config = CacheConfigReader()
        self.__headers, self.__auth = {'Content-Type': 'application/json'}, (
            self.__test_rail_config.user, self.__test_rail_config.api_key)

    @property
    def cases(self) -> list[TestCase]:
        return self.__get_cases()

    @property
    def runs(self) -> list[TestRun]:
        return self.__get_runs()

    def get_failed_tests_defects_list(self, failed_tests_ids_list: list[int]) -> list[TestInRunResults]:
        cached_file_name = os.path.join(CACHED_INFO_DIR_PATH, "cached_failed_tests_results.txt")
        tests_with_defects_list = []

        if self.__cache_config.use_cached_failed_tests_results:
            tests_with_defects_list = read_list_of_dicts_from_file(cached_file_name)

        if not tests_with_defects_list:
            for test_id in failed_tests_ids_list:
                failed_test_results = requests.get(
                    f'{self.__test_rail_config.api_address}/get_results/{test_id}', headers=self.__headers,
                    auth=self.__auth).json()

                [tests_with_defects_list.append(TestInRunResults(test_id, failed_test)) for failed_test in
                 failed_test_results]

            write_list_of_dicts_to_file(cached_file_name,
                                        [test_result.full_info for test_result in tests_with_defects_list])

        return tests_with_defects_list

    def get_failed_tests(self) -> list[TestInRun]:
        tests_in_run_list = self.get_test_results_from_all_test_runs()
        failed_test_status_id = 5
        failed_tests_list = [test_in_run for test_in_run in tests_in_run_list if
                             test_in_run.status_id == failed_test_status_id]

        return failed_tests_list

    def get_tests_in_run(self, run_id: int) -> list[TestInRun]:
        response = requests.get(f'{self.__test_rail_config.api_address}/get_tests/{run_id}',
                                headers=self.__headers,
                                auth=self.__auth)

        return [TestInRun(test) for test in response.json()]

    def get_test_results_from_all_test_runs(self) -> TestInRun:
        cached_file_name = os.path.join(CACHED_INFO_DIR_PATH, "cached_tests_in_runs.txt")
        list_with_all_tests_results = []

        if self.__cache_config.use_cached_tests_results:
            list_with_all_tests_results = [TestInRun(list_element) for list_element in
                                           read_list_of_dicts_from_file(cached_file_name)]

        if not list_with_all_tests_results:
            list_with_test_runs_results_lists = []

            for run in self.runs:
                tests_in_run_list = self.get_tests_in_run(run.id)
                list_with_test_runs_results_lists.append(tests_in_run_list)

            # get one giant list of all tests results
            list_with_all_tests_results = list(itertools.chain.from_iterable(list_with_test_runs_results_lists))
            write_list_of_dicts_to_file(cached_file_name,
                                        [test_result.full_info for test_result in list_with_all_tests_results])
            print(f"Information about all tests in test runs is saved to {cached_file_name} file")

        return list_with_all_tests_results

    def get_test_cases_list_by_id_list(self, id_list: int) -> list[TestCase]:
        return [case for case in self.cases if case.id in id_list]

    def __get_cases(self) -> list[TestCase]:
        print("Getting information about all test cases...")
        cached_file_name = os.path.join(CACHED_INFO_DIR_PATH, "cached_cases.txt")
        test_cases_list = []

        if self.__cache_config.use_cached_cases:
            test_cases_list = [TestCase(case) for case in read_list_of_dicts_from_file(cached_file_name)]

        if not test_cases_list:
            # If test cases were never being loaded or setting "use_cached_test_cases" is false ->
            # send request to TestRail
            response = requests.get(
                f'{self.__test_rail_config.api_address}/get_cases/{self.__test_rail_config.project_id}&suite_id={self.__test_rail_config.suite_id}',
                headers=self.__headers,
                auth=self.__auth)

            cases_list = [TestCase(case) for case in response.json()]
            test_cases_list = [case for case in cases_list if not case.is_deleted]
            write_list_of_dicts_to_file(cached_file_name, [case.full_info for case in test_cases_list])

            print(f"Information about test cases is saved to {cached_file_name} file")

        return test_cases_list

    def __get_runs(self) -> list[TestRun]:
        print("Getting information about all test runs...")
        cached_file_name = os.path.join(CACHED_INFO_DIR_PATH, "cached_test_runs_info.txt")
        test_runs_list = []

        if self.__cache_config.use_cached_runs:
            test_runs_list = [TestRun(run) for run in read_list_of_dicts_from_file(cached_file_name)]

        if not test_runs_list:
            # If test runs were never being loaded or setting "use_cached_test_runs" is false ->
            # send request to TestRail
            response = requests.get(
                f'{self.__test_rail_config.api_address}/get_runs/{self.__test_rail_config.project_id}',
                headers=self.__headers,
                auth=self.__auth)

            test_runs_list = [TestRun(run) for run in response.json()]
            write_list_of_dicts_to_file(cached_file_name, [test_run.full_info for test_run in test_runs_list])

            print(f"Information about test runs is saved to {cached_file_name} file")

        return test_runs_list
