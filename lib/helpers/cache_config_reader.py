import os

import yaml

from path_constants import CONFIGS_DIR_PATH


class CacheConfigReader:
    def __init__(self):
        with open(os.path.join(CONFIGS_DIR_PATH, "cache-config.yaml"),
                  "r") as stream:
            try:
                self.__config = yaml.load(stream, Loader=yaml.FullLoader)["use_cache"]
            except yaml.YAMLError as exc:
                print(exc)

    @property
    def use_cached_cases(self):
        return self.__config["use_cached_test_cases"]

    @property
    def use_cached_runs(self):
        return self.__config["use_cached_test_runs"]
