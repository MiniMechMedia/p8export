import unittest
import pathlib
from src.FileRegistry import TestFileEnum, TempFileEnum
import shutil
import os


class BaseTest(unittest.TestCase):
    def assertContentsEqual(self, actual: str, expected: TestFileEnum):
        self.assertEqual(actual, self.getTestFileContents(expected))

    def assertFilesEqual(self, actual: TempFileEnum, expected: TestFileEnum):
        self.assertContentsEqual(
            actual=self.getTempFileContents(actual), expected=expected
        )

    def getTestFilePath(self, testFileName: TestFileEnum) -> pathlib.Path:
        # return testFileName.filepath
        return pathlib.Path("test/" + testFileName.value)

    def getTempFilePath(self, tempFileName: TempFileEnum) -> pathlib.Path:
        return pathlib.Path("tmp/" + tempFileName.value)

    def getTestFileContents(self, testFileName: TestFileEnum) -> str:
        with open(self.getTestFilePath(testFileName=testFileName)) as file:
            return file.read()

    def getTestFileBytes(self, testFileName: TestFileEnum) -> bytes:
        with open(self.getTestFilePath(testFileName=testFileName), "rb") as file:
            return file.read()

    def getTempFileBytes(self, tempFileName: TempFileEnum) -> bytes:
        with open(self.getTempFilePath(tempFileName), "rb") as file:
            return file.read()

    def getTempFileContents(self, tempFileName: TempFileEnum) -> str:
        with open(self.getTempFilePath(tempFileName), "r") as file:
            return file.read()


#     tmp file
