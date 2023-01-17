import collections
import itertools
import json
from collections import Counter

import requests

from config_reader import TestRailConfig
from test_case import TestCase
from test_in_run import TestInRun
from test_run import TestRun

test_rail_config = TestRailConfig()
api_key = test_rail_config.api_key
api_address = test_rail_config.api_address
project_id = test_rail_config.project_id
suite_id = test_rail_config.suite_id
headers, auth = {'Content-Type': 'application/json'}, (test_rail_config.user, api_key)


class ApiRequests:
    __cases = None
    __runs = None

    @property
    def cases(self):
        if self.__cases is None:
            self.__cases = self.__get_cases()

        return self.__cases

    @property
    def runs(self):
        if self.__runs is None:
            self.__runs = self.__get_runs()

        return self.__runs

    def __get_cases(self):
        response = requests.get(f'{api_address}/get_cases/{project_id}&suite_id={suite_id}',
                                headers=headers,
                                auth=auth)

        cases_list = [TestCase(case) for case in response.json()]
        return [case for case in cases_list if not case.is_deleted]

    def get_results_for_case(self, run_id, case_id):
        response = requests.get(f'{api_address}/get_results_for_case/{run_id}/{case_id}',
                                headers=headers,
                                auth=auth)

        return response.json()

    def __get_tests_in_run(self, run_id):
        response = requests.get(f'{api_address}/get_tests/{run_id}',
                                headers=headers,
                                auth=auth)

        return [TestInRun(test) for test in response.json()]

    def __get_runs(self):
        response = requests.get(f'{api_address}/get_runs/{project_id}',
                                headers=headers,
                                auth=auth)

        return [TestRun(run) for run in response.json()]

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
        with open('output_files/never_executed_test_cases.txt', 'w') as f:
            for test_case in cases_list:
                f.write(f"{test_case.title} {test_case.link}")

        print("Finished! Please check output_files/never_executed_test_cases.txt file")

    def __get_case(self, case_id):
        response = requests.get(f'{api_address}/get_case/{case_id}',
                                headers=headers,
                                auth=auth)

        return TestCase(response.json())

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

    def get_most_failing_test_cases(self):
        print("Getting the most failing test cases in test runs...")
        test_id_list = []

        # Get IDs of failing tests in test runs
        for run in self.runs:
            failed_status_id = 5
            failed_tests_list = requests.get(
                f'{api_address}/get_results_for_run/{run.id}&status_id={failed_status_id}',
                headers=headers,
                auth=auth).json()
            test_id_list.append([failed_test["test_id"] for failed_test in failed_tests_list])

        # Chain all lists of failed tests into one array
        chained_failed_tests_list = list(itertools.chain.from_iterable(test_id_list))

        # Write all failed tests for debugging
        with open('cached_info/all_failed_tests.txt', 'w') as f:
            for failed_test in chained_failed_tests_list:
                f.write(f"{failed_test}\n")

        # Use reading of cached chained_failed_tests_list for debugging
        with open("cached_info/all_failed_tests.txt") as f:
            chained_failed_tests_list = f.read().splitlines()

        case_info_list = []
        # Get test case ID and name
        for test_id in chained_failed_tests_list:
            test_id_number = int(test_id)
            response = requests.get(f'{api_address}/get_test/{test_id_number}',
                                    headers=headers,
                                    auth=auth).json()
            case_id = response["case_id"]
            case_title = response["title"]
            case_info_list.append({"case_id": case_id, "case_title": case_title})

        # Write all cases IDs tests for debugging
        f = open('cached_info/failed_case_ids.txt', 'w')
        for failed_case_id in case_info_list:
            f.write(json.dumps(failed_case_id))

        with open("cached_info/failed_case_ids.txt") as f:
            chained_failed_tests_list = f.read().splitlines()
            case_info_list = json.loads("[" + chained_failed_tests_list[0].replace("}{", "}, {") + "]")

        # count how many times one unique test case was used
        case_ids_list = [case["case_id"] for case in case_info_list]
        test_case_usages_counter = collections.Counter(case_ids_list)
        most_common_info = test_case_usages_counter.most_common()

        with open('output_files/the_most_failing_test_cases_in_test_runs.txt', 'w') as f:
            for info in most_common_info:
                case_title = list(filter(lambda element: element["case_id"] == info[0], case_info_list))[0][
                    "case_title"]

                f.write(f"{info[0]} {case_title}: {info[1]} times\n")

        print("Finished! Please check output_files/the_most_failing_test_cases_in_test_runs.txt file")

    def __get_case_from_cached_list(self, case_id):
        id = [case for case in self.cases if case.id == case_id]

        if id and len(id) > 0:
            return id[0]
        else:
            return None

    def __get_cases_list_from_cached_list(self, case_ids_list):
        cases_list = [self.__get_case_from_cached_list(case_id) for case_id in case_ids_list]

        return [case for case in cases_list if case and not case.is_deleted]
