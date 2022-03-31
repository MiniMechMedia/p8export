from BaseTest import BaseTest
from src.ParsedContents import ParsedContents
from src.ParsedContents import Pico8FileParser

from FileRegistry import TestFileEnum


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
