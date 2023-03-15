import pytest

from lib.api_requests import ApiRequests
from lib.test_rail_objects.test_case import TestCase


@pytest.fixture
def api_requests() -> ApiRequests:
    return ApiRequests()


@pytest.mark.parametrize("return_value", [[TestCase({'id': 111111111, "is_deleted": 0, 'title': 'Export'}),
                                           TestCase({'id': 111111110, "is_deleted": 0, 'title': 'Validation'})]
                                          ])
def test_cases_are_not_empty(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_response_about_all_test_cases", return_value=return_value)
    mocker.patch.object(api_requests, "_cache_test_cases_info")

    assert len(api_requests.cases) > 0


@pytest.mark.parametrize("return_value", [[]])
def test_cases_are_empty_when_test_rail_req_returned_nothing(api_requests, mocker, return_value):
    mocker.patch.object(api_requests, "_get_response_about_all_test_cases", return_value=return_value)
    mocker.patch.object(api_requests, "_cache_test_cases_info")

    assert len(api_requests.cases) == 0


def test_runs_are_not_empty(api_requests):
    assert len(api_requests.runs) > 0


def test_results_from_all_runs_are_not_empty(api_requests):
    assert len(api_requests.test_results_from_all_runs) > 0


def test_failed_tests_are_not_empty(api_requests):
    assert len(api_requests.failed_tests) > 0


def test_get_failed_tests_defects_list_is_not_empty(api_requests):
    failed_test_ids_list = [285085986, 285085926, 285085917, 285085919, 285085908]
    assert len(api_requests.get_failed_tests_defects_list(failed_test_ids_list)) > 0
