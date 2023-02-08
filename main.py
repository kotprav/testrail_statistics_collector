from lib.tool_api import ToolApi

get_never_executed_test_cases = True
get_most_failing_test_cases = True
get_the_buggiest_test_cases = True

api_requests = ToolApi()

if get_never_executed_test_cases:
    not_executed_test_cases_list = api_requests.get_not_executed_cases_list()

if get_most_failing_test_cases:
    api_requests.get_most_failing_test_cases()

if get_the_buggiest_test_cases:
    api_requests.get_the_buggiest_tests()

print("Thanks for using this tool :3")
