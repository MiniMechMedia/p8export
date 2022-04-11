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
    ITCH_DESCRIPTION_EVALUATED_FILE = "../test/testFiles/itch-description-evaluated.md"
    ORCHESTRATION_TEST_FILE = "../test/testFiles/orchestration-test.p8"
    BASIC_DESCRIPTION_EVALUATED_FILE = (
        "../test/testFiles/basic-description-evaluated.md"
    )
    # HTML_EXPORT_TEST_FILE_JS = "index.js"
    # HTML_EXPORT_TEMP_FILE_HTML = "index.html"
    # P8_PNG_EXPORT_TEST_FILE = "something.png"
    AGGREGATE_README_BEFORE_FILE = (
        "../test/testFiles/readmeTestFiles/readme-for-three-games.md"
    )
    AGGREGATE_README_AFTER_UPDATE_FILE = (
        "../test/testFiles/readmeTestFiles/readme-for-three-games-expected-update.md"
    )

    @property
    def value(self):
        return super().value


class TempFileEnum(FileEnum):
    LABEL_IMAGE_TEMP_FILE = "label.png"
    ITCH_COVER_IMAGE_TEMP_FILE = "cover.png"
    ITCH_DESCRIPTION_EVALUATED_FILE = "itch-description-evaluated-temp.md"
    HTML_EXPORT_TEMP_DIR = "html_export/"
    HTML_EXPORT_TEMP_FILE_HTML = "html_export/index.html"
    HTML_EXPORT_TEMP_FILE_JS = "html_export/index.js"
    HTML_EXPORT_TEMP_FILE_ZIP = "html_export/index.zip"
    P8_PNG_EXPORT_TEMP_FILE = "mongo-bongo.p8.png"
    AGGREGATE_README_UPDATED_AFTER = "readme-for-three-games-updated.md"
    # ORCHESTRATION_TEMP_DIR = 'orch/'
    # ORCHESTRATION_BASIC_FILE


class TemplateFileEnum(FileEnum):
    ITCH_GAME_DESCRIPTION_MD = "template/game-cart-itch-description.md"
    ITCH_TWEET_DESCRIPTION_MD = "template/tweet-cart-itch-description.md"
    README_GAME_MD = "template/game-readme.md"
    README_TWEET_MD = "template/tweet-readme.md"
    AGGREGATE_README_MD = "template/aggregate-readme.md"
