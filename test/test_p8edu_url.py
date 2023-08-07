from test.BaseTest import BaseTest
from src.Pico8EduUrlCompliationTarget import Pico8EduUrlCompilationTarget
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents, Metadata, ControlEnum
from src.FileRegistry import TestFileEnum, TempFileEnum

class TestP8EduUrl(BaseTest):
    def test_can_create_minified_source(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        result = Pico8EduUrlCompilationTarget.createMinifiedCartContents(parsedContents)
        assert parsedContents.minifiedSourceCode in result

    def test_can_create_rom(self):
        parsedContents = self.parseFile(TestFileEnum.TWEET_CART_ANNOTATED_TEST_FILE)
        result = Pico8EduUrlCompilationTarget.writeFullRomMinified(
            parsedContents.config,
            parsedContents
        )
        # assert parsedContents.minifiedSourceCode in result
        self.assertFileExists(TempFileEnum.TWEET_CART_MINIFIED_ROM)
