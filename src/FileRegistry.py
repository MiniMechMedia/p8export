from enum import Enum


class TestFileEnum(Enum):
    YAML_TEST_FILE = "../test/testFiles/yaml-test.p8"
    COVER_IMAGE_TEST_FILE = "../test/testFiles/label-image-exists-test.p8"
    ITCH_COVER_IMAGE_TEST_FILE = "../test/testFiles/cover.png"
    LABEL_MISSING_TEST_FILE = "../test/testFiles/label-image-missing-test.p8"
    LABEL_IMAGE_TEST_FILE = "../test/testFiles/label.png"
    BASIC_GAME_TEMPLATE_FILE = "../test/testFiles/basic-game-template.p8"
    TWEET_CART_TEMPLATE_FILE = "../test/testFiles/tweet-cart-template.p8"


class TempFileEnum(Enum):
    LABEL_IMAGE_TEMP_FILE = "label.png"
    ITCH_COVER_IMAGE_TEMP_FILE = "cover.png"


class TemplateFileEnum(Enum):
    Something = ""
