from BaseTest import BaseTest
from FileRegistry import TestFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents, MetaData


class TestParsing(BaseTest):
    def test_parsing(self):
        parsed: ParsedContents = Pico8FileParser.parse(
            self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        )

    def test_parsing_metadata(self):
        contents: str = self.getTestFileContents(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(contents)
        parsedYaml: dict = Pico8FileParser.parseYamlFromRawYaml(rawYaml)
        metadata: MetaData = Pico8FileParser.parseMetadata(parsedYaml)
