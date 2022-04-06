import unittest
import pathlib
from src.FileRegistry import TestFileEnum, TempFileEnum
import shutil
import os


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            shutil.rmtree("tmp/")
        except FileNotFoundError:
            pass

        os.makedirs("tmp/")

    def assertContentsEqual(self, actual: str, expected: TestFileEnum):
        self.assertEqual(actual, self.getTestFileContents(expected))

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


#     tmp file
