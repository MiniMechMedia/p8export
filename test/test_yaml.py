from test.BaseTest import BaseTest
from src.pico8fileparser import Pico8FileParser

from src.FileRegistry import TestFileEnum


class TestYaml(BaseTest):
    def test_can_parse_raw_yaml(self):
        # parsed: ParsedContents = ParsedContents.fromPath(
        #     self.getTestFilePath("yaml-test.p8")
        # )
        rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(
            self.getTestFileContents(TestFileEnum.YAML_TEST_FILE)
        )

        self.assertEqual(
            rawYaml,
            """
# Embed: 750 x 680
game_name: XXXXX
# Leave blank to use game-name
game_slug:
        """.strip(),
        )

    def test_can_parse_structured_yaml(self):
        rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(
            self.getTestFileContents(TestFileEnum.YAML_TEST_FILE)
        )

        parsedYaml: dict = Pico8FileParser.parseYamlFromRawYaml(rawYaml)

        self.assertEqual(parsedYaml, {"game_name": "XXXXX", "game_slug": None})
