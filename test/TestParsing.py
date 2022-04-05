from BaseTest import BaseTest
from FileRegistry import TestFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents


class TestParsing(BaseTest):
    def test_parsing(self):
        parsed: ParsedContents = Pico8FileParser.parseFileEntirely(
            self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        )
