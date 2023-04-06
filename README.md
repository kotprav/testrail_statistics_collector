**Configuration**

1. `test-rail-config.yaml` file
Please add `test-rail-config.yaml` file with the information needed:

`
testrail:
    server_address: "https://testrail.something.com"
    api_address: "https://testrail.something.com/index.php?/api/v2"
    project_id: "123"
    suite_id: "1234" # Test run that tracks failed tests and links them with bugs (workaround for not connected TestRail and JIRA)
    authentication:
        user: "user@something.com"
        api_key: "some_api_key"
`

2. `main.py`
Update the state of variables if needed to disable some tool functionality
   1. `GET_NEVER_EXECUTED_TEST_CASES`
   2. `GET_MOST_FAILING_TEST_CASES`
   3. `GET_MOST_BUGGIEST_TEST_CASES`
