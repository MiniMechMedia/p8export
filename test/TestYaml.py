from BaseTest import BaseTest
from src.ParsedContents import ParsedContents
import pathlib


class TestYaml(BaseTest):
    def test_can_parse_raw_yaml(self):
        parsed: ParsedContents = ParsedContents.fromPath(
            self.getTestFilePath("yaml-test.p8")
        )

        self.assertEqual(
            parsed.getRawYaml(),
            """
# Embed: 750 x 680
game_name: XXXXX
# Leave blank to use game-name
game_slug:
        """.strip(),
        )
