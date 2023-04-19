**Description**

This tool helps to get:

1. Never executed test cases in TestRail -- test cases that were never executed in TestRail **test runs**.
2. The most frequently failing test cases in TestRail. Bugs should be added to "**Defects**" field, when a test case is
   marked as failed in a TestRail **test run**.
3. Bugs that affect fail test cases the most. Bugs should be added to "**Defects**" field, when a test case is marked as
   failed in a TestRail **test run**.

**Configuration**

1. `test-rail-config.yaml` file

Please add `test-rail-config.yaml` file with the information needed:

```
testrail:
    server_address: "https://testrail.something.com"
    api_address: "https://testrail.something.com/index.php?/api/v2"
    project_id: "123"
    suite_id: "1234" # Test run that tracks failed tests and links them with bugs (workaround for not connected TestRail and JIRA)
    authentication:
        user: "user@something.com"
        api_key: "some_api_key"
```

2. `main.py`

Update the state of variables if needed to disable some tool functionality

1. `GET_NEVER_EXECUTED_TEST_CASES`
2. `GET_THE_MOST_FAILING_TEST_CASES`
3. `GET_THE_MOST_IRRITATING_BUGS`

**Results**

When the tool finishes its job, output files are generated in `output_files` directory. If you used 3 features, these
files are generated:

1. `never_executed_test_cases.txt`
2. `the_most_failing_test_cases_in_test_runs.txt`
3. `the_worst_bugs.txt`
