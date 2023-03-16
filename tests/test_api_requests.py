import pytest

from lib.api_requests import ApiRequests
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_run import TestRun


@pytest.fixture
def api_requests() -> ApiRequests:
    return ApiRequests()


def test_cases_are_not_empty(api_requests, mocker):
    first_test_case_info = {'id': 1, 'title': 'Happy Test Case #1', 'section_id': 2, 'template_id': 3,
                            'type_id': 4, 'priority_id': 5, 'milestone_id': None, 'refs': None, 'created_by': 6,
                            'created_on': 1632745653, 'updated_by': 7, 'updated_on': 1642690096, 'estimate': None,
                            'estimate_forecast': None, 'suite_id': 8, 'display_order': 9, 'is_deleted': 0,
                            'custom_status': 1, 'custom_preconds': None, 'custom_steps': None,
                            'custom_steps_separated': [
                                {'content': 'Shared Steps #1',
                                 'expected': 'Happy life', 'additional_info': '',
                                 'refs': ''}], 'custom_mission': None, 'custom_session_charter': None}

    second_test_case_info = {'id': 2, 'title': '"Happy Test Case #2',
                             'section_id': 3, 'template_id': 4, 'type_id': 5, 'priority_id': 1,
                             'milestone_id': None, 'refs': None, 'created_by': 6, 'created_on': 1669623477,
                             'updated_by': 7, 'updated_on': 1670314544, 'estimate': None, 'estimate_forecast': None,
                             'suite_id': 8, 'display_order': 9, 'is_deleted': 0}

    return_value = [TestCase(first_test_case_info), TestCase(second_test_case_info)]

    mocker.patch.object(api_requests, "_get_response_about_all_test_cases", return_value=return_value)
    mocker.patch.object(api_requests, "_cache_test_cases_info")

    assert len(api_requests.cases) > 0


@pytest.mark.parametrize("return_value", [[]])
def test_cases_are_empty_when_test_rail_req_returned_nothing(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_response_about_all_test_cases", return_value=return_value)
    mocker.patch.object(api_requests, "_cache_test_cases_info")

    assert len(api_requests.cases) == 0


def test_runs_are_not_empty(api_requests, mocker):
    first_run_info = {'id': 1, 'suite_id': 2, 'name': 'Test Run #1', 'description': None, 'milestone_id': 1,
                      'assignedto_id': None, 'include_all': False, 'is_completed': False, 'completed_on': None,
                      'config': None, 'config_ids': [], 'passed_count': 0, 'blocked_count': 0, 'untested_count': 3,
                      'retest_count': 0, 'failed_count': 0, 'custom_status1_count': 0, 'custom_status2_count': 0,
                      'custom_status3_count': 0, 'custom_status4_count': 0, 'custom_status5_count': 0,
                      'custom_status6_count': 0, 'custom_status7_count': 0, 'project_id': 1, 'plan_id': None,
                      'created_on': 1678963570, 'updated_on': 1678963570, 'refs': 'JIRA-1111', 'created_by': 1,
                      'url': 'https://testrail.hello.com/index.php?/runs/view/1'}

    second_run_info = {'id': 2, 'suite_id': 2, 'name': 'Test Run #2',
                       'description': None, 'milestone_id': 3, 'assignedto_id': None, 'include_all': False,
                       'is_completed': False,
                       'completed_on': None, 'config': None, 'config_ids': [], 'passed_count': 0, 'blocked_count': 0,
                       'untested_count': 4, 'retest_count': 0, 'failed_count': 0, 'custom_status1_count': 0,
                       'custom_status2_count': 0, 'custom_status3_count': 0, 'custom_status4_count': 0,
                       'custom_status5_count': 0,
                       'custom_status6_count': 0, 'custom_status7_count': 0, 'project_id': 5, 'plan_id': None,
                       'created_on': 1678963301, 'updated_on': 1678963301, 'refs': 'JIRA-2222', 'created_by': 3,
                       'url': 'https://testrail.hello.com/index.php?/runs/view/2'}

    return_value = [TestRun(first_run_info), TestRun(second_run_info)]
    mocker.patch.object(api_requests, "_get_response_about_all_test_runs", return_value=return_value)
    mocker.patch.object(api_requests, "_cache_run_info")

    assert len(api_requests.runs) > 0


@pytest.mark.parametrize("return_value", [[]])
def test_runs_are_empty_when_test_rail_req_returned_nothing(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_response_about_all_test_runs", return_value=return_value)
    mocker.patch.object(api_requests, "_cache_run_info")

    assert len(api_requests.runs) == 0

# def test_results_from_all_runs_are_not_empty(api_requests):
#     assert len(api_requests.test_results_from_all_runs) > 0
#
#
# def test_failed_tests_are_not_empty(api_requests):
#     assert len(api_requests.failed_tests) > 0
#
#
# def test_get_failed_tests_defects_list_is_not_empty(api_requests):
#     failed_test_ids_list = [285085986, 285085926, 285085917, 285085919, 285085908]
#     assert len(api_requests.get_failed_tests_defects_list(failed_test_ids_list)) > 0
