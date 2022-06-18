from BaseTest import BaseTest
from src.FileRegistry import TestFileEnum, TempFileEnum
from pathlib import Path
from src.pico8fileparser import Pico8FileParser
from src.ParsedContents import ParsedContents#, Metadata, ControlEnum
from src.P8FileTransformerCompilationTarget import P8FileTransformerCompilationTarget

class TestP8FileTransformation(BaseTest):
    def testCanSwapOutPlaceholderComments(self):
        contents: str = self.getTestFilePath(TestFileEnum.GAME_CART_TEST_FILE).read_text()
        copyLoc: Path = self.getTempFilePath(TempFileEnum.GAME_CART_TEST_FILE_TRANSFORMED_COPY_LOCATION)
        copyLoc.write_text(
            data = contents
        )
        parsed: ParsedContents = Pico8FileParser.parse(filePath=copyLoc)
        P8FileTransformerCompilationTarget.transformP8File(p8FilePath=copyLoc, parsed=parsed)
        self.assertFilesEqual(
            actual=TempFileEnum.GAME_CART_TEST_FILE_TRANSFORMED_COPY_LOCATION,
            expected=TestFileEnum.GAME_CART_TEST_FILE_TRANSFORMED_EXPECTED
        )

    def testGameDescriptionCommentsAreIdempotent(self):
        pass

    def testGameDescriptionCommentsCanBeAdded(self):
        pass



