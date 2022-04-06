from enum import Enum
from pathlib import Path


class FileEnum(Enum):
    @property
    def filepath(self) -> Path:
        return Path(self.value)

    def readBinary(self) -> bytes:
        with open(self.value, "rb") as file:
            return file.read()

    def readText(self) -> str:
        with open(self.value, "r") as file:
            return file.read()

    def writeBinary(self, content: bytes) -> None:
        with open(self.value, "wb") as file:
            file.write(content)

    def writeText(self, content: str) -> None:
        with open(self.value, "w") as file:
            file.write(content)


# TODO move this into a separate file in test/
class TestFileEnum(FileEnum):
    YAML_TEST_FILE = "../test/testFiles/yaml-test.p8"
    COVER_IMAGE_TEST_FILE = "../test/testFiles/label-image-exists-test.p8"
    ITCH_COVER_IMAGE_TEST_FILE = "../test/testFiles/cover.png"
    LABEL_MISSING_TEST_FILE = "../test/testFiles/label-image-missing-test.p8"
    LABEL_IMAGE_TEST_FILE = "../test/testFiles/label.png"
    BASIC_GAME_TEMPLATE_FILE = "../test/testFiles/basic-game-template.p8"
    TWEET_CART_TEMPLATE_FILE = "../test/testFiles/tweet-cart-template.p8"
    TWEET_CART_TEMPLATE_EVALUATED_DESCRIPTION_FILE = (
        "../test/testFiles/tweet-cart-template-evaluated-description.md"
    )

    @property
    def value(self):
        return super().value


class TempFileEnum(FileEnum):
    LABEL_IMAGE_TEMP_FILE = "label.png"
    ITCH_COVER_IMAGE_TEMP_FILE = "cover.png"


class TemplateFileEnum(FileEnum):
    ITCH_DESCRIPTION_MD = "../template/itchDescription.md"
