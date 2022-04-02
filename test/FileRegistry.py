from enum import Enum


class TestFileEnum(Enum):
    YAML_TEST_FILE = "testFiles/yaml-test.p8"
    COVER_IMAGE_TEST_FILE = "testFiles/label-image-exists-test.p8"
    ITCH_COVER_IMAGE_TEST_FILE = "testFiles/cover.png"
    LABEL_MISSING_TEST_FILE = "testFiles/label-image-missing-test.p8"
    LABEL_IMAGE_TEST_FILE = "testFiles/label.png"


class TempFileEnum(Enum):
    LABEL_IMAGE_TEMP_FILE = "label.png"
    ITCH_COVER_IMAGE_TEMP_FILE = "cover.png"
