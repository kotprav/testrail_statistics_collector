import os

import yaml

from path_constants import CONFIGS_DIR_PATH


class TestRailConfigReader:
    @property
    def api_key(self) -> str:
        return self._get_config()["authentication"]["api_key"]

    @property
    def user(self) -> str:
        return self._get_config()["authentication"]["user"]

    @property
    def api_address(self) -> str:
        return self._get_config()["api_address"]

    @property
    def server_address(self) -> str:
        return self._get_config()["server_address"]

    @property
    def project_id(self) -> str:
        return self._get_config()["project_id"]

    @property
    def suite_id(self) -> str:  # pragma: no cover
        return self._get_config()["suite_id"]

    def _get_config(self):  # pragma: no cover
        with open(os.path.join(CONFIGS_DIR_PATH, "test-rail-config.yaml"),
                  "r") as stream:
            try:
                return yaml.load(stream, Loader=yaml.FullLoader)["testrail"]
            except yaml.YAMLError as exc:
                print(exc)
