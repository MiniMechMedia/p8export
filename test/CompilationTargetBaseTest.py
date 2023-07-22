from test.BaseTest import BaseTest
from src.ParsedContents import ParsedContents
from src.FileRegistry import TestFileEnum
from src.pico8fileparser import Pico8FileParser


class CompilationTargetBaseTest(BaseTest):
    def parseTestFile(self, testFile: TestFileEnum):
        return Pico8FileParser.parse(self.getTestFilePath(testFile))
