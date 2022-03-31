import unittest
import pathlib
from FileRegistry import TestFileEnum


class BaseTest(unittest.TestCase):
    def getTestFilePath(self, testFileName: TestFileEnum) -> pathlib.Path:
        return pathlib.Path("test/" + testFileName.value)

    def getTestFileContents(self, testFileName: TestFileEnum) -> str:
        with open(self.getTestFilePath(testFileName=testFileName)) as file:
            return file.read()
