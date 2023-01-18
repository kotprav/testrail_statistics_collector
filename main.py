from lib.api_requests import ApiRequests

get_test_cases_count, get_runs_count = True, True
get_never_executed_test_cases = False
get_most_failing_test_cases = False
get_the_buggiest_test_cases = True

api_requests = ApiRequests()

if get_test_cases_count:
    print(f"Test cases count: {len(api_requests.cases)}")

if get_runs_count:
    print(f"Test runs count: {len(api_requests.runs)}")

if get_never_executed_test_cases:
    not_executed_test_cases_list = api_requests.get_not_executed_cases_list()

if get_most_failing_test_cases:
    api_requests.get_most_failing_test_cases()

if get_the_buggiest_test_cases:
    api_requests.get_the_buggiest_test_cases()

pass
