import pytest

from lib.api_requests import ApiRequests
from lib.test_rail_objects.test_case import TestCase
from lib.test_rail_objects.test_in_run import TestInRun
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

    second_test_case_info = {'id': 2, 'title': 'Happy Test Case #2',
                             'section_id': 3, 'template_id': 4, 'type_id': 5, 'priority_id': 1,
                             'milestone_id': None, 'refs': None, 'created_by': 6, 'created_on': 1669623477,
                             'updated_by': 7, 'updated_on': 1670314544, 'estimate': None, 'estimate_forecast': None,
                             'suite_id': 8, 'display_order': 9, 'is_deleted': 0}

    return_value = [TestCase(first_test_case_info), TestCase(second_test_case_info)]

    mocker.patch.object(api_requests, "_get_response_about_all_test_cases", return_value=return_value)
    cases = api_requests.cases

    assert len(cases) == 2
    first_case_res = cases[0]
    assert first_case_res.id == 1
    assert first_case_res.is_deleted == 0
    assert "/cases/view/1" in first_case_res.link
    assert first_case_res.title == 'Happy Test Case #1'
    assert first_case_res.full_info

    seconds_case_res = cases[1]
    assert seconds_case_res.id == 2
    assert seconds_case_res.is_deleted == 0
    assert "/cases/view/2" in seconds_case_res.link
    assert seconds_case_res.title == 'Happy Test Case #2'
    assert seconds_case_res.full_info


@pytest.mark.parametrize("return_value", [[]])
def test_cases_are_empty_when_test_rail_req_returned_nothing(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_response_about_all_test_cases", return_value=return_value)

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

    runs = api_requests.runs
    assert len(runs) == 2

    first_test_run = runs[0]
    second_test_run = runs[1]
    assert first_test_run.id == 1
    assert second_test_run.id == 2

    assert first_test_run.full_info == {"id": 1}
    assert second_test_run.full_info == {"id": 2}


@pytest.mark.parametrize("return_value", [[]])
def test_runs_are_empty_when_test_rail_req_returned_nothing(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_response_about_all_test_runs", return_value=return_value)

    assert len(api_requests.runs) == 0


def test_results_from_all_runs_are_not_empty(api_requests, mocker):
    first_test_info = {'id': 111111111, 'case_id': 333333333, 'status_id': 5, 'defects': ["JIRA-1234"]}
    second_test_info = {'id': 222222222, 'case_id': 444444444, 'status_id': 6, 'defects': []}

    return_value: list[TestInRun] = [TestInRun(first_test_info), TestInRun(second_test_info)]
    mocker.patch.object(api_requests, "_get_test_runs_results", return_value=return_value)

    test_results_from_all_runs = api_requests.get_test_results_from_all_runs()
    first_run_results = test_results_from_all_runs[0]
    second_run_results = test_results_from_all_runs[1]
    assert len(test_results_from_all_runs) == 2

    assert first_run_results.case_id == 333333333
    assert first_run_results.defects == ["JIRA-1234"]
    assert first_run_results.id == 111111111
    assert first_run_results.status_id == 5
    assert first_run_results.full_info == {'id': 111111111, 'case_id': 333333333, 'status_id': 5,
                                           'defects': ['JIRA-1234']}

    assert second_run_results.case_id == 444444444
    assert second_run_results.defects == []
    assert second_run_results.id == 222222222
    assert second_run_results.status_id == 6
    assert second_run_results.full_info == {'id': 222222222, 'case_id': 444444444, 'status_id': 6, 'defects': []}


@pytest.mark.parametrize("return_value", [[]])
def test_results_from_all_runs_are_empty_when_test_rail_req_returned_nothing(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_test_runs_results", return_value=return_value)

    assert len(api_requests.get_test_results_from_all_runs()) == 0


def test_failed_tests_are_not_empty(api_requests, mocker):
    first_failed_test_info = {'id': 111111111, 'case_id': 333333333, 'status_id': 5,
                              'defects': ['JIRA-1234']}
    second_not_failed_test_info = {'id': 222222222, 'case_id': 444444444, 'status_id': 6, 'defects': []}
    third_failed_test_info = {'id': 111111112, 'case_id': 333333330, 'status_id': 5, 'defects': []}

    return_value: list[TestInRun] = [TestInRun(first_failed_test_info), TestInRun(second_not_failed_test_info),
                                     TestInRun(third_failed_test_info)]
    mocker.patch.object(api_requests, "get_test_results_from_all_runs", return_value=return_value)

    failed_tests_results = api_requests.failed_tests

    assert len(failed_tests_results) == 2

    first_failed_run_results = failed_tests_results[0]
    second_failed_run_results = failed_tests_results[1]

    assert first_failed_run_results.case_id == 333333333
    assert first_failed_run_results.defects == ['JIRA-1234']
    assert first_failed_run_results.id == 111111111
    assert first_failed_run_results.status_id == 5
    assert first_failed_run_results.full_info == {'id': 111111111, 'case_id': 333333333, 'status_id': 5,
                                                  'defects': ['JIRA-1234']}

    assert second_failed_run_results.case_id == 333333330
    assert second_failed_run_results.defects == []
    assert second_failed_run_results.id == 111111112
    assert second_failed_run_results.status_id == 5
    assert second_failed_run_results.full_info == {'id': 111111112, 'case_id': 333333330, 'status_id': 5, 'defects': []}


def test_failed_test_results_from_all_runs_are_empty_when_no_results(api_requests, mocker):
    mocker.patch.object(api_requests, "get_test_results_from_all_runs", return_value=[])

    assert len(api_requests.failed_tests) == 0


def test_get_failed_tests_defects_list_is_not_empty(api_requests, mocker):
    first_failed_test_result = [{'id': 1111111111, 'test_id': 1212121212, 'status_id': 5, 'created_on': 1678968274,
                                 'assignedto_id': None,
                                 'comment': None, 'version': None, 'elapsed': None, 'defects': 'JIRA-123',
                                 'created_by': 2948,
                                 'custom_step_results': [{
                                     'content': 'Step 1',
                                     'expected': '', 'actual': '', 'additional_info': '', 'refs': '', 'status_id': 3},
                                     {'content': 'Step 2',
                                      'expected': 'Expected 2',
                                      'actual': '', 'additional_info': '', 'refs': '', 'status_id': 3},
                                     {'content': 'Step 3',
                                      'expected': 'Expected 3',
                                      'actual': '', 'additional_info': '', 'refs': '', 'status_id': 3},
                                     {
                                         'content': 'Step 4',
                                         'expected': 'Expected 4',
                                         'actual': '', 'additional_info': '', 'refs': '', 'status_id': 3}, {
                                         'content': 'Content 4',
                                         'expected': 'Expected 4',
                                         'actual': '', 'additional_info': '', 'refs': '', 'status_id': 3}],
                                 'attachment_ids': []}]

    mocker.patch.object(api_requests, "_get_failed_test_results_response",
                        return_value=first_failed_test_result)
    failed_tests_defects_list = api_requests.get_failed_tests_defects_list([1111111111])

    assert len(failed_tests_defects_list) == 1
    failed_test_defects = failed_tests_defects_list[0]
    assert failed_test_defects.case_id is None
    assert failed_test_defects.defects == 'JIRA-123'
    assert failed_test_defects.full_info == {'id': 1212121212, 'case_id': None, 'status_id': 5, 'defects': 'JIRA-123'}
    assert failed_test_defects.id == 1212121212
    assert failed_test_defects.status_id == 5


def test_get_failed_tests_defects_list_is_empty_when_no_results_returned(api_requests, mocker):
    mocker.patch.object(api_requests, "_get_failed_test_results_response",
                        return_value=[])

    assert len(api_requests.get_failed_tests_defects_list([])) == 0
