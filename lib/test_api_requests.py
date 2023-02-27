import pytest

from lib.api_requests import ApiRequests


@pytest.fixture
def api_requests() -> ApiRequests:
    return ApiRequests()


def test_cases_are_not_empty(api_requests):
    assert len(api_requests.cases) > 0


def test_runs_are_not_empty(api_requests):
    assert len(api_requests.runs) > 0


def test_results_from_all_runs_are_not_empty(api_requests):
    assert len(api_requests.test_results_from_all_runs) > 0


def test_failed_tests_are_not_empty(api_requests):
    assert len(api_requests.failed_tests) > 0


def test_get_failed_tests_defects_list_is_not_empty(api_requests):
    failed_test_ids_list = [285085986, 285085926, 285085917, 285085919, 285085908]
    assert len(api_requests.get_failed_tests_defects_list(failed_test_ids_list)) > 0
