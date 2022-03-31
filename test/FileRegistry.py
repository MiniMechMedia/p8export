from enum import Enum


class TestFileEnum(Enum):
    YAML_TEST_FILE = "testFiles/yaml-test.p8"
    COVER_IMAGE_TEST_FILE = "testFiles/label-image-exists-test.p8"
    LABEL_MISSING_TEST_FILE = "testFiles/label-image-missing-test.p8"
