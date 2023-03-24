from lib.test_rail_objects.test_in_run import TestInRun

shared_fields = {'id': 4444444444, 'test_id': 555554444, 'status_id': 5, 'created_on': 1679575288,
                 'assignedto_id': None, 'comment': None, 'version': None, 'elapsed': None, 'defects': 'JIRA-0001',
                 'created_by': 11, 'custom_step_results': [
        {'content': 'Step 1', 'expected': '', 'actual': '', 'additional_info': '',
         'refs': '', 'status_id': 3},
        {'content': 'Step 2', 'expected': '', 'actual': '', 'additional_info': '',
         'refs': '', 'status_id': 3},
        {'content': 'Step 3', 'expected': 'Expected 3', 'actual': '',
         'additional_info': '', 'refs': '', 'status_id': 3}, ], 'attachment_ids': []}


def test_defects_are_returned_and_parsed_if_valid_one_ticket_received():
    defect = "JIRA-0001"
    shared_fields["defects"] = defect
    test_in_run = TestInRun(shared_fields)

    assert test_in_run.defects == defect


def test_defects_are_returned_and_parsed_if_valid_multiple_tickets_received():
    shared_fields["defects"] = "JIRA-0001, JIRA-0002"
    test_in_run = TestInRun(shared_fields)

    assert test_in_run.defects == ['JIRA-0001', 'JIRA-0002']


def test_defects_are_returned_as_empty_list_if_empty_info():
    defect = ""
    shared_fields["defects"] = defect
    test_in_run = TestInRun(shared_fields)

    assert test_in_run.defects == []


def test_defects_are_returned_if_object_without_defects_sent():
    empty_object = {}
    test_in_run = TestInRun(empty_object)

    assert test_in_run.defects == []
