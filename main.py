from lib.tool_api import ToolApi

get_never_executed_test_cases = True
get_most_failing_test_cases = False
get_the_buggiest_test_cases = False

api_requests = ToolApi()

print("Hello ฅ՞•ﻌ•՞ฅ")

if get_never_executed_test_cases:
    not_executed_test_cases_list = api_requests.get_not_executed_cases_list()

if get_most_failing_test_cases:
    api_requests.get_most_failing_test_cases()

if get_the_buggiest_test_cases:
    api_requests.get_the_buggiest_tests()

