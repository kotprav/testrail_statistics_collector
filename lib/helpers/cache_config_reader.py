import os

import yaml

from path_constants import CONFIGS_DIR_PATH


class CacheConfigReader:
    def __init__(self):
        with open(os.path.join(CONFIGS_DIR_PATH, "cache-config.yaml"),
                  "r") as stream:
            try:
                self.__config = yaml.load(stream, Loader=yaml.FullLoader)["use_cached"]
            except yaml.YAMLError as exc:
                print(exc)

    @property
    def use_cached_cases(self):
        return self.__config["test_cases"]

    @property
    def use_cached_runs(self):
        return self.__config["test_runs"]

    @property
    def use_cached_tests_results(self):
        return self.__config["tests_in_test_runs"]

    @property
    def use_cached_failed_tests_results(self):
        return self.__config["failed_tests_results"]
