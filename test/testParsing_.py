from BaseTest import BaseTest
from src.FileRegistry import TestFileEnum
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents, Metadata, ControlEnum


class TestParsing(BaseTest):
    # def test_parsing(self):
    #     parsed: ParsedContents = Pico8FileParser.parse(
    #         self.getTestFilePath(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
    #     )

    def test_parsing_metadata(self):
        # contents: str = self.getTestFileContents(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)
        # rawYaml: str = Pico8FileParser.parseRawYamlFromFileContents(contents)
        # parsedYaml: dict = Pico8FileParser.parseYamlFromRawYaml(rawYaml)
        # metadata: MetaData = Pico8FileParser.parseMetadata(parsedYaml)
        parsed: ParsedContents = self.parseFile(TestFileEnum.BASIC_GAME_TEMPLATE_FILE)

        firstJam: Metadata.JamInfo = parsed.metadata.jam_info[0]
        self.assertEqual(firstJam.jam_name, "TriJam")
        self.assertEqual(firstJam.jam_number, -1)

        secondJam: Metadata.JamInfo = parsed.metadata.jam_info[1]
        self.assertEqual(secondJam.jam_name, "MiniJam")
        self.assertEqual(secondJam.jam_number, None)

        firstControl: Metadata.Control = parsed.metadata.controls[0]
        self.assertEqual(firstControl.inputs, [ControlEnum.ARROW_KEYS])
        secondControl: Metadata.Control = parsed.metadata.controls[1]
        self.assertEqual(secondControl.inputs, [ControlEnum.X, ControlEnum.Z])

    def test_parsing_sourcecode(self):
        parsed: ParsedContents = self.parseFile(TestFileEnum.TWEET_CART_TEMPLATE_FILE)

        self.assertEqual(parsed.sourceCodeP8sciiCharCount, 277)
