from enum import Enum
from pathlib import Path

root = Path(__file__).parent.parent
# raise Exception(root)


class FileEnum(Enum):
    @property
    def filepath(self) -> Path:
        return Path(self.value)

    def readBinary(self) -> bytes:
        with open(self.value, "rb") as file:
            return file.read()

    def readText(self) -> str:
        # import pathlib
        # raise Exception(pathlib.Path(self.value).absolute())
        with open(self.value, "r") as file:
            return file.read()

    def writeBinary(self, content: bytes) -> None:
        with open(self.value, "wb") as file:
            file.write(content)

    def writeText(self, content: str) -> None:
        with open(self.value, "w") as file:
            file.write(content)

    # GAME_ITCH_DESCRIPTION = "template/game-cart-itch-description.html.md"
    # TWEET_ITCH_DESCRIPTION = "template/tweet-cart-itch-description.html.md"
    # GAME_GITHUB_README = "template/game-readme.md"
    # TWEET_GITHUB_README = 'template/tweet-readme.md'
    # # README_TWEET_MD = "template/tweet-readme.md"
    # AGGREGATE_GITHUB_README = "template/aggregate-readme.md"


# TODO move this into a separate file in test/
class TestFileEnum(FileEnum):
    YAML_TEST_FILE = root / "test/testFiles/yaml-test.p8"
    COVER_IMAGE_TEST_FILE = root / "test/testFiles/label-image-exists-test.p8"
    ITCH_COVER_IMAGE_TEST_FILE = root / "test/testFiles/cover.png"
    LABEL_MISSING_TEST_FILE = root / "test/testFiles/label-image-missing-test.p8"
    LABEL_IMAGE_TEST_FILE = root / "test/testFiles/label.png"

    GAME_CART_TEST_FILE = root / "test/testFiles/game-cart-test-file.p8"
    TWEET_CART_TEST_FILE = root / "test/testFiles/tweet-cart-test-file.p8"
    TWEET_CART_ANNOTATED_TEST_FILE = (
        root / "test/testFiles/tweet-cart-annotated-test-file.p8"
    )

    TWEET_STRING_TEMPLATE_EXPECTED = (
        root / "test/expectedRender/tweet-string-template-expected.md"
    )
    GAME_STRING_TEMPLATE_EXPECTED = (
        root / "test/expectedRender/game-string-template-expected.md"
    )
    GAME_ITCH_DESCRIPTION_EXPECTED = (
        root / "test/expectedRender/game-itch-description-expected.html"
    )
    TWEET_GITHUB_README_EXPECTED = (
        root / "test/expectedRender/tweet-github-readme-expected.md"
    )
    GAME_GITHUB_README_EXPECTED = (
        root / "test/expectedRender/game-github-readme-expected.md"
    )

    TWEET_ITCH_DESCRIPTION_EXPECTED = (
        root / "test/expectedRender/tweet-itch-description-expected.html"
    )

    ORCHESTRATION_TEST_FILE = root / "test/testFiles/orchestration-test.p8"

    # HTML_EXPORT_TEST_FILE_JS = "index.js"
    # HTML_EXPORT_TEMP_FILE_HTML = "index.html"
    # P8_PNG_EXPORT_TEST_FILE = "something.png"
    AGGREGATE_README_BEFORE_FILE = (
        root / "test/testFiles/readmeTestFiles/readme-for-three-games.md"
    )
    AGGREGATE_README_AFTER_UPDATE_FILE = (
        root / "test/testFiles/readmeTestFiles/readme-for-three-games-expected-update.md"
    )
    AGGREGATE_README_AFTER_ADD_FILE = (
        root / "test/testFiles/readmeTestFiles/readme-for-three-games-expected-added.md"
    )

    GAME_CART_TEST_FILE_TRANSFORMED_EXPECTED = (
        root / "test/expectedTransformation/game-cart-test-file-transformed-expected.p8"
    )

    @property
    def value(self):
        return super().value


class TempFileEnum(FileEnum):
    LABEL_IMAGE_TEMP_FILE = "label.png"
    ITCH_COVER_IMAGE_TEMP_FILE = "cover.png"
    HTML_EXPORT_TEMP_DIR = "html_export/"
    HTML_EXPORT_TEMP_FILE_HTML = "html_export/index.html"
    HTML_EXPORT_TEMP_FILE_JS = "html_export/index.js"
    HTML_EXPORT_TEMP_FILE_ZIP = "html_export/index.zip"
    P8_PNG_EXPORT_TEMP_FILE = "mongo-bongo.p8.png"

    AGGREGATE_GITHUB_README_UPDATED_ACTUAL = "aggregate-github-readme-updated-actual.md"
    AGGREGATE_GITHUB_README_ADDED_ACTUAL = "aggregate-github-readme-added-actual.md"

    GAME_ITCH_DESCRIPTION_ACTUAL = "game-itch-description-actual.html"
    TWEET_ITCH_DESCRIPTION_ACTUAL = "tweet-itch-description-actual.html"
    GAME_GITHUB_README_ACTUAL = "game-github-readme-actual.md"
    TWEET_GITHUB_README_ACTUAL = "tweet-github-readme-actual.md"
    # TWEET_TINY_ROM_ACTUAL
    # ORCHESTRATION_TEMP_DIR = 'orch/'
    # ORCHESTRATION_BASIC_FILE

    GAME_CART_TEST_FILE_TRANSFORMED_COPY_LOCATION = (
        "game-cart-test-file-transformed-copy-location.p8"
    )

    TWEET_CART_MINIFIED = 'tweetMinified.p8'
    TWEET_CART_MINIFIED_ROM = 'tweetMinified.p8.rom'

    MULTIPLE_EXPORT_README = "p8export-test/test_can_export_multiple_games/README.md"


class TemplateFileEnum(FileEnum):
    GAME_ITCH_DESCRIPTION_TEMPLATE = (
        root / "template/game-itch-description-template.html.md"
    )
    TWEET_ITCH_DESCRIPTION_TEMPLATE = (
        root / "template/tweet-itch-description-template.html.md"
    )
    GAME_GITHUB_README_TEMPLATE = root / "template/game-github-readme-template.md"
    TWEET_GITHUB_README_TEMPLATE = root / "template/tweet-github-readme-template.md"
    # README_TWEET_MD = "template/tweet-readme.md"
    AGGREGATE_GITHUB_README_TEMPLATE = (
        root / "template/aggregate-github-readme-template.md"
    )
