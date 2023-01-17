import os

import yaml

from path_constants import CONFIGS_DIR_PATH


class TestRailConfigReader:
    def __init__(self):
        with open(os.path.join(CONFIGS_DIR_PATH, "test-rail-config.yaml"),
                  "r") as stream:
            try:
                self.__config = yaml.load(stream, Loader=yaml.FullLoader)["testrail"]
            except yaml.YAMLError as exc:
                print(exc)

    @property
    def api_key(self):
        return self.__config["authentication"]["api_key"]

    @property
    def user(self):
        return self.__config["authentication"]["user"]

    @property
    def api_address(self):
        return self.__config["api_address"]

    @property
    def server_address(self):
        return self.__config["server_address"]

    @property
    def project_id(self):
        return self.__config["project_id"]

    @property
    def suite_id(self):
        return self.__config["suite_id"]
