import itertools
import os

import requests

from lib.helpers.cache_config_reader import CacheConfigReader
from lib.helpers.file_helper import read_list_of_dicts_from_file, write_list_of_dicts_to_file
from lib.helpers.test_rail_config_reader import TestRailConfigReader
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun
from lib.test_rail_objects.test_run import TestRun
from path_constants import CACHED_INFO_DIR_PATH


class ApiRequests:  # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.__test_rail_config = TestRailConfigReader()
        self.__cache_config = CacheConfigReader()
        self.__headers, self.__auth = {'Content-Type': 'application/json'}, (
            self.__test_rail_config.user, self.__test_rail_config.api_key)
        self.__cases = None
        self.__runs = None
        self.__tests_with_defects_list: list[TestInRun] = []
        self.__list_with_all_tests_results: list[TestInRun] = []
        self.__failed_tests_list: list[TestInRun] = []
        self.__request_timeout_time = 5

    @property
    def cases(self) -> list[TestCase]:
        if not self.__cases:
            self.__cases = self._get_cases()
        return self.__cases

    @property
    def runs(self) -> list[TestRun]:
        if not self.__runs:
            self.__runs = self._get_runs()
        return self.__runs

    def get_test_results_from_all_runs(self) -> list[TestInRun]:
        if not self.__list_with_all_tests_results:
            self.__list_with_all_tests_results = self._get_test_results_from_all_test_runs()
        return self.__list_with_all_tests_results

    @property
    def failed_tests(self) -> list[TestInRun]:
        if not self.__failed_tests_list:
            self.__failed_tests_list = self._get_failed_tests()

        return self.__failed_tests_list

    def get_failed_tests_defects_list(self, failed_tests_ids_list: list[int]) -> list[TestInRun]:
        cached_file_name: str = os.path.join(CACHED_INFO_DIR_PATH, "cached_failed_tests_results.txt")
        if self.__cache_config.use_cached_failed_tests_results:
            self.__tests_with_defects_list = [TestInRun(test_with_defect) for test_with_defect in
                                              read_list_of_dicts_from_file(cached_file_name)]  # pragma: no cover

        if not self.__tests_with_defects_list:
            self.__tests_with_defects_list = self._get_failed_test_results(failed_tests_ids_list)
            self._cache_failed_tests_defects_list(cached_file_name)

        return self.__tests_with_defects_list

    def _get_failed_test_results(self, failed_tests_ids_list: list[int]) -> list[TestInRun]:
        test_results_list: list[TestInRun] = []
        for test_id in failed_tests_ids_list:
            failed_test_results = self._get_failed_test_results_response(test_id)

            for failed_test in failed_test_results:
                failed_test["id"] = failed_test["test_id"]
                failed_test_in_run = TestInRun(failed_test)

                if failed_test_in_run not in test_results_list:
                    test_results_list.append(failed_test_in_run)

        return test_results_list

    def _cache_failed_tests_defects_list(self, cached_file_name):
        write_list_of_dicts_to_file(cached_file_name,
                                    [test_result.full_info for test_result in
                                     self.__tests_with_defects_list])  # pragma: no cover

    def _get_failed_test_results_response(self, test_id: int):  # pragma: no cover
        failed_test_results = requests.get(
            f'{self.__test_rail_config.api_address}/get_results/{test_id}', headers=self.__headers,
            auth=self.__auth, timeout=self.__request_timeout_time).json()

        self._write_network_logs(f"Request to get results of failed test with id {test_id} was sent")

        return failed_test_results

    def _get_tests_in_run(self, run_id: int) -> list[TestInRun]:  # pragma: no cover
        response = requests.get(f'{self.__test_rail_config.api_address}/get_tests/{run_id}',
                                headers=self.__headers,
                                auth=self.__auth, timeout=self.__request_timeout_time)

        self._write_network_logs(f"Request to get tests in run with ID {run_id} was sent")

        return [TestInRun(test) for test in response.json()]

    def _get_failed_tests(self) -> list[TestInRun]:
        self._write_network_logs("Getting test results from all test runs")
        failed_test_status_id = 5
        failed_tests_list: list[TestInRun] = [test_in_run for test_in_run in self.get_test_results_from_all_runs() if
                                              test_in_run.status_id == failed_test_status_id]

        return failed_tests_list

    def _get_test_results_from_all_test_runs(self) -> list[TestInRun]:  # pragma: no cover
        cached_file_name: str = os.path.join(CACHED_INFO_DIR_PATH, "cached_tests_in_runs.txt")

        if self.__cache_config.use_cached_tests_results:
            return [TestInRun(list_element) for list_element in
                    read_list_of_dicts_from_file(cached_file_name)]

        self._write_network_logs(f"Getting available information about tests from {len(self.runs)} test runs")

        # get one giant list of all tests results from multiple lists
        all_tests_results_list: list[TestInRun] = self._get_test_runs_results()
        self._cache_all_tests_results(all_tests_results_list, cached_file_name)

        return all_tests_results_list

    def _cache_all_tests_results(self, all_tests_results_list: list[TestInRun],
                                 cached_file_name: str):  # pragma: no cover
        write_list_of_dicts_to_file(cached_file_name,
                                    [test_result.full_info for test_result in all_tests_results_list])

        self._write_network_logs(f"Information about all tests in test runs is saved to {cached_file_name} file")

    def _get_test_runs_results(self) -> list[TestInRun]:  # pragma: no cover
        list_with_test_runs_results_lists: list[list[TestInRun]] = [self._get_tests_in_run(run.id) for run in
                                                                    self.runs]

        return list(itertools.chain.from_iterable(list_with_test_runs_results_lists))

    def _get_cases(self) -> list[TestCase]:  # pragma: no cover
        self._write_network_logs("Getting information about all test cases...")
        cached_file_name: str = os.path.join(CACHED_INFO_DIR_PATH, "cached_cases.txt")
        test_cases_list: list[TestCase] = []

        if self.__cache_config.use_cached_cases:
            test_cases_list = [TestCase(case) for case in read_list_of_dicts_from_file(cached_file_name)]

        if not test_cases_list:
            # If test cases were never being loaded or setting "use_cached_test_cases" is false ->
            # send request to TestRail
            cases_list: list[TestCase] = self._get_response_about_all_test_cases()
            test_cases_list = [case for case in cases_list if not case.is_deleted]
            self._cache_test_cases_info(cases_list, cached_file_name)

        return test_cases_list

    def _get_response_about_all_test_cases(self) -> list[TestCase]:  # pragma: no cover
        response = requests.get(
            f'{self.__test_rail_config.api_address}/get_cases/{self.__test_rail_config.project_id}&suite_id={self.__test_rail_config.suite_id}',
            headers=self.__headers,
            auth=self.__auth, timeout=self.__request_timeout_time)

        self._write_network_logs("Request to get cases was sent and received")
        return [TestCase(case) for case in response.json()]

    def _cache_test_cases_info(self, cases_list: list[TestCase], cached_file_name: str):  # pragma: no cover
        write_list_of_dicts_to_file(cached_file_name, [case.full_info for case in cases_list])
        self._write_network_logs(f"Information about test cases is saved to {cached_file_name} file")

    def _get_runs(self) -> list[TestRun]:  # pragma: no cover
        self._write_network_logs("Getting information about all test runs...")
        cached_file_name: str = os.path.join(CACHED_INFO_DIR_PATH, "cached_test_runs_info.txt")
        test_runs_list: list[TestRun] = []

        if self.__cache_config.use_cached_runs:
            test_runs_list = [TestRun(run) for run in read_list_of_dicts_from_file(cached_file_name)]

        if not test_runs_list:
            test_runs_list = self._get_response_about_all_test_runs()
            # If test runs were never being loaded or setting "use_cached_test_runs" is false ->
            # send request to TestRail
            self._cache_run_info(test_runs_list, cached_file_name)

        return test_runs_list

    def _cache_run_info(self, test_runs_list: list[TestRun], cached_file_name: str):
        write_list_of_dicts_to_file(cached_file_name, [test_run.full_info for test_run in test_runs_list])
        self._write_network_logs(f"Information about test runs available is saved to {cached_file_name} file")

    def _get_response_about_all_test_runs(self) -> list[TestRun]:
        response = requests.get(
            f'{self.__test_rail_config.api_address}/get_runs/{self.__test_rail_config.project_id}',
            headers=self.__headers,
            auth=self.__auth, timeout=self.__request_timeout_time)

        self._write_network_logs("Request to get runs was sent and received")

        return [TestRun(run) for run in response.json()]

    @staticmethod
    def _write_network_logs(message: str):
        print(f'---Network: {message}')
