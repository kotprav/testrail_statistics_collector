"""
Path constants used across the app.
"""
import os

MAIN_PROJECT_DIR_PATH = os.path.dirname(__file__)
CACHED_INFO_DIR_PATH = os.path.join(MAIN_PROJECT_DIR_PATH, 'cached_info')
CONFIGS_DIR_PATH = os.path.join(MAIN_PROJECT_DIR_PATH, 'configs')
LIB_DIR_PATH = os.path.join(MAIN_PROJECT_DIR_PATH, 'lib')
OUTPUT_FILES_DIR_PATH = os.path.join(MAIN_PROJECT_DIR_PATH, 'output_files')
