"""
Main file to work with the tool.
"""
from lib.tool_api import ToolApi

GET_NEVER_EXECUTED_TEST_CASES = True
GET_THE_MOST_FAILING_TEST_CASES = True
GET_THE_BUGGIEST_TEST_CASES = True

api_requests = ToolApi()

print("Hello ฅ՞•ﻌ•՞ฅ")

if GET_NEVER_EXECUTED_TEST_CASES:
    api_requests.save_not_executed_cases_list()

if GET_THE_MOST_FAILING_TEST_CASES:
    api_requests.save_most_failing_test_cases()

if GET_THE_BUGGIEST_TEST_CASES:
    api_requests.save_the_buggiest_tests()
