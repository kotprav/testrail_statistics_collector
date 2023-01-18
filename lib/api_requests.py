import itertools
import json
import os

import requests

from lib.helpers.cache_config_reader import CacheConfigReader
from lib.helpers.file_helper import read_list_of_dicts_from_file, write_list_of_dicts_to_file
from lib.helpers.test_rail_config_reader import TestRailConfigReader
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun
from lib.test_rail_objects.test_run import TestRun
from path_constants import CACHED_INFO_DIR_PATH


class ApiRequests:
    __failed_tests_file_name = os.path.join(CACHED_INFO_DIR_PATH, "all_failed_tests.txt")

    def __init__(self):
        self.__test_rail_config = TestRailConfigReader()
        self.__cache_config = CacheConfigReader()
        self.__headers, self.__auth = {'Content-Type': 'application/json'}, (
            self.__test_rail_config.user, self.__test_rail_config.api_key)

    @property
    def cases(self):
        return self.__get_cases()

    @property
    def runs(self):
        return self.__get_runs()

    def get_test_case_info(self, test_ids_list):
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

    def get_failed_tests_defects_list(self, failed_tests_ids_list):
        tests_with_defects_list = []

        for test_id in failed_tests_ids_list:
            failed_tests_list = requests.get(
                f'{self.__test_rail_config.api_address}/get_results/{test_id}', headers=self.__headers,
                auth=self.__auth).json()

            for failed_test in failed_tests_list:
                tests_with_defects_list.append({"test_id": test_id, "defects": failed_test["defects"]})

        return tests_with_defects_list

    def get_failed_tests_ids(self):
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

    def get_tests_in_run(self, run_id):
        response = requests.get(f'{self.__test_rail_config.api_address}/get_tests/{run_id}',
                                headers=self.__headers,
                                auth=self.__auth)

        return [TestInRun(test) for test in response.json()]

    def __get_cases(self):
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

    def __get_runs(self):
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
